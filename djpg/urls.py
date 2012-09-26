from django.conf.urls import patterns, url

pagseguro_urlpatterns = patterns('djpg.views',
	url(r'^pagseguro/notifications/$', 'notifications',
		name='pagseguro_notifications'),
)
