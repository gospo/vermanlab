# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

urlpatterns = patterns('cert.views',
	url(r'^$', 'cert', name='cert'),
)