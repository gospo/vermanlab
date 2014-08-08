# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

urlpatterns = patterns('upload.views',
    url(r'^$', 'upload', name='upload'),
)