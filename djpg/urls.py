from django.conf.urls import url
from .views import notifications

urlpatterns = [
    url(r'notifications/$', notifications, name='pagseguro_notifications'),
]
