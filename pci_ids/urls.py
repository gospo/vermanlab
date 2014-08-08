# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from pci_ids import views

urlpatterns = patterns('',
    url(r'^$', views.pci_ids.as_view()),
)