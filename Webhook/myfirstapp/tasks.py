import requests
from celery import shared_task
from .models import Webhook
from celery import shared_task
from celery.utils.log import get_task_logger
from celery.exceptions import MaxRetriesExceededError
from time import sleep


logger = get_task_logger(__name__)

@shared_task(bind=True, max_retries=5)
def trigger_event(self, company_id):  
    active_webhooks = Webhook.objects.get(company_id=company_id)
    # active_webhooks = Webhook.objects.filter(company_id=company_id, is_active=True)
    for webhook in active_webhooks:
        try:
            response = requests.post(webhook.url, headers=webhook.headers)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(e)
            continue


