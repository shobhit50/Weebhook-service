from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Webhook
from .Serializer import WebhookSerializer
from .tasks import trigger_event
from django.http import HttpResponse
import requests
import pdb; 





@api_view(['GET', 'POST'])
def webhooks(request):
    if request.method == 'GET':
        webhooks = Webhook.objects.all()
        serializer = WebhookSerializer(webhooks, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = WebhookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def webhook_detail(request, pk):
    try:
        webhook = Webhook.objects.get(pk=pk)
    except Webhook.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = WebhookSerializer(webhook)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = WebhookSerializer(webhook, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        webhook.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
def fire_event(request):
    data = request.data.get('company_id')
    if data is None:
        return HttpResponse("Missing company_id in request data", status=400)
    
    trigger_event.delay(data)
    return HttpResponse("Event triggered", status=200)

    