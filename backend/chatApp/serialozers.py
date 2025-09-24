from rest_framework import serializers
from .models import  AiChatSession, AiRequest

class AiChatSessionSerializer(serializers.Serializer):
    role = serializers.CharField(max_length=10)
    content = serializers.CharField()

class AiRequestSerializer(serializers.ModelSerializer):
    messages = AiChatSessionSerializer(many=True)
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Flatten the messages list
        representation['messages'] = [msg for sublist in representation['messages'] for msg in sublist]
        return representation
    class Meta:
        model = AiRequest
        fields = ['id', 'messages'] 
        read_only_fields = [ 'messages']   
    