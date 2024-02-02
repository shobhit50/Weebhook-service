from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Webhook
from .Serializer import WebhookSerializer
from .tasks import trigger_event 
from django.http import HttpResponse
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist



@api_view(['GET'])
def root(request):
    return Response({
        "webhooks": {
        "create": "POST /webhooks/",
        "update": "PATCH /webhooks/{id}/",
        "delete": "DELETE /webhooks/{id}/",
        "listing": "GET /webhooks/",
        "singleGet": "GET /webhooks/{id}/"
    },
        "fire_event": "/fire_event/"
    })

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
    company_id = request.data.get('company_id')
    if company_id is None:
        return HttpResponse("Missing company_id in request data", status=400)
    try:
        webhook = Webhook.objects.get(company_id=company_id)
        if not webhook.is_active:
            return HttpResponse("Webhook is not active", status=400)
        if settings.USE_CELERY:
            # Use Celery to fire event
            print("triggering celery function")
            trigger_event.delay(webhook.url) 
            return HttpResponse("Event triggered", status=200)
        else:
            # Use normal function to fire event
            print("triggering normal function")
            trigger_event(webhook.url)
            return HttpResponse("Event triggered", status=200)
    except ObjectDoesNotExist:
        return HttpResponse("Webhook with company_id' does not exist.", status=400)

    