from django.contrib import admin
from .models import AiChatSession, AiRequest

# Register your models here.
admin.site.register(AiChatSession)
admin.site.register(AiRequest)