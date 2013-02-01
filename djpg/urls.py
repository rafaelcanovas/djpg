from django.conf.urls import patterns, url

urlpatterns = patterns('djpg.views',
	url(r'notifications/$', 'notifications', name='pagseguro_notifications'),
)
