from celery import shared_task

@shared_task
def process_ai_request(ai_request_id):
    from .models import  AiRequest

    try:
        ai_request = AiRequest.objects.get(id=ai_request_id)
        ai_request.handle()
    except AiRequest.DoesNotExist:
        # Handle the case where the AiRequest does not exist
        pass
