# -*- coding: utf-8 -*-
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver

class KernelTarball(models.Model):
    tarToBeAdded = models.FileField(upload_to='to_be_added')
    expandedKernelFolder = models.FileField(upload_to='added')
    # returns the KernelVersion name
    def __unicode__(self):
		no_path_name = self.expandedKernelFolder.name.split('/')[-1]
		return unicode(no_path_name[:-7])

# Receive the pre_delete signal and delete the file associated with the model instance.
@receiver(post_delete, sender=KernelTarball)
def kernel_tarball_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    instance.tarToBeAdded.delete(False)
    instance.expandedKernelFolder.delete(False)

class ShellScript(models.Model):
    modInfoTreeScript = models.FileField(upload_to='scripts')

    def __unicode__(self):
		no_path_name = self.modInfoTreeScript.name.split('/')[-1]
		return unicode(no_path_name[:-3])

# Receive the pre_delete signal and delete the file associated with the model instance.
@receiver(post_delete, sender=ShellScript)
def shell_script_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    instance.modInfoTreeScript.delete(False)
