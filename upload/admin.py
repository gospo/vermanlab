from django.contrib import admin
from upload.models import KernelTarball
from upload.models import ShellScript

# Register your models here.
admin.site.register(KernelTarball)
admin.site.register(ShellScript)