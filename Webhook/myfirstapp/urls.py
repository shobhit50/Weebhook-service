from django.urls import path
from . import views
from django.urls import path
from . import views

urlpatterns = [
    path('', views.root, name='root'),
    path('webhooks/', views.webhooks, name='webhooks-list-create'),
    path('webhooks/<int:pk>/', views.webhook_detail, name='webhook-detail'),
    path('fire_event', views.fire_event, name='fire-event'),
   
]