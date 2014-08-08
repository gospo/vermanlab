from django.contrib import admin
from schema.models import KernelVersion, Module, Aliases

# Register your models here.
admin.site.register(KernelVersion)
admin.site.register(Module)
admin.site.register(Aliases)