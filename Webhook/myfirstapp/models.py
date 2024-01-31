from django.db import models




class Data(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=500)

class Webhook(models.Model):
    id = models.AutoField(primary_key=True)
    company_id = models.CharField(max_length=100)
    url = models.URLField()
    headers = models.JSONField(blank=True, null=True)
    events = models.JSONField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)