import requests
from celery import shared_task
from .models import Webhook
from celery import shared_task
from celery.utils.log import get_task_logger
from celery.exceptions import MaxRetriesExceededError
from time import sleep
from django.core.exceptions import ObjectDoesNotExist


logger = get_task_logger(__name__)




@shared_task(bind=True, max_retries=5)
def trigger_event(self, webhook_url):  
    try:
        response = requests.post(webhook_url)
        if response.status_code == 200:
            print(f"Successfully triggered webhook at {webhook_url}")
            return f"Successfully triggered webhook at {webhook_url}"
        else:
            print(f"Failed to trigger webhook at {webhook_url}. Status code: {response.status_code}")
            return f"Failed to trigger webhook at {webhook_url}. Status code: {response.status_code}"
    except ObjectDoesNotExist:
        return f"Error occurred while trying to trigger webhook at {webhook_url}"


    