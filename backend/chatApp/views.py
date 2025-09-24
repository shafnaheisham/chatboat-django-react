from django.shortcuts import render, redirect
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .models import AiChatSession, AiRequest
from .serialozers import AiChatSessionSerializer, AiRequestSerializer
from django.shortcuts import get_object_or_404


@api_view(['POST'])
def create_chat_session(request):
    """Create a new AI chat session"""
    session = AiChatSession.objects.create()
    serializer = AiChatSessionSerializer(session)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['POST','GET'])
def chat_session(request, session_id):
    """Handle chat session interactions"""
    session = get_object_or_404(AiChatSession, id=session_id)
    
    if request.method == 'POST':
        message = request.data.get('message')
        if not message:
            return Response({"error": "Message is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        session.send(message)
        last_request = session.get_last_requet()
        if last_request:
            last_request._que_job()
            serializer = AiRequestSerializer(last_request)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "Unable to create AI request."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    elif request.method == 'GET':
        requests = session.requests.all().order_by('-created_at')
        serializer = AiRequestSerializer(requests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
