from django.db import models
from openai import OpenAI
from .tasks import process_ai_request


# Create your models here.
class AiChatSession(models.Model):
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def get_last_requet(self):
        return self.airequest_set.all().order_by('-created_at').first()
    
    def _create_message(self,message,role="user"):
        return {"role": role,"content": message}
    
    def _create_first_message(self,message):
        return [ self._create_message("You are a helpful assistant that helps people find information.","system"),
                self._create_message(message,"user")] 
    
    def messages(self):
        all_messages=[]
        request=self.get_last_requet()
        if request:
            all_messages.append(request.messages)
            try:
                all_messages.append(request.response['choices'][0]['message'])
            except(KeyError,TypeError,IndexError):
                pass
        return all_messages
    
    def send(self,message):
        """send a message to the AI and create a new request"""
        last_request=self.get_last_requet()
        if not last_request:
            AiRequest.objects.create(
            session=self,
            message=self._create_message(message,"user"))
        elif last_request and last_request.status in [AiRequest.completed,AiRequest.failed]:    
            AiRequest.objects.create(
            session=self,
            messages=self.messages()+[self._create_message(message,"user")])
        else:
            return 

class AiRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('running', 'Running'),]
    status=models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    session = models.ForeignKey(AiChatSession, on_delete=models.CASCADE, related_name='requests',null=True,blank=True)
    messages=models.JSONField()
    response=models.JSONField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def _que_job(self):
        process_ai_request.delay(self.id)
    def handle(self):
        self.status='running'
        self.save()
        client=OpenAI()
        try:
            completion=client.chat.completions.create(
                model="gpt-4o-mini",
                messages=self.messages
            )
            self.response=completion
            self.status='completed'
        except Exception as e:
            self.response={'error':str(e)}
            self.status='failed'
        self.save()    
    def save(self, *args, **kwargs):
        is_new=self._state.adding
        super().save(*args, **kwargs)
        if is_new:
            self._que_job()    