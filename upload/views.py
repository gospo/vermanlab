# -*- coding: utf-8 -*-
import os, subprocess

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from mysite import settings

from upload.models import KernelTarball
from upload.models import ShellScript
from upload.forms import KernelTarballForm

from schema.models import KernelVersion, Module, Aliases

def upload(request):

    # Load documents for the list page
    kernel_tarballs = KernelTarball.objects.all()
    shell_script = ShellScript.objects.get(modInfoTreeScript="scripts/vmlModInfoTreeCreation.sh")

    # Handle file upload
    if request.method == 'POST':
        form = KernelTarballForm(request.POST, request.FILES)
        if form.is_valid():
            new_kernel_tarball = KernelTarball(tarToBeAdded = request.FILES['toBeAdded'], expandedKernelFolder = request.FILES['toBeAdded'])
            # save the files, one in to_be_added, one in added
            new_kernel_tarball.save()

            unzip_file(new_kernel_tarball)
            new_kernel_tarball.tarToBeAdded.delete()
            return HttpResponseRedirect(reverse('upload.views.upload'))
    else:
        form = KernelTarballForm() # A file uploaded unbounded to the file name

    # Render list page with the documents and the form
    return render_to_response(
        'upload/upload.html',
        {'shell_script': shell_script, 'kernel_tarballs': kernel_tarballs, 'form': form},
        context_instance=RequestContext(request)
    )

def unzip_file(kernel_object):
    added_folder_path = os.path.join(settings.MEDIA_ROOT, 'added/')
    file_path = os.path.join(settings.MEDIA_ROOT, kernel_object.expandedKernelFolder.name)
    
    
    os.system('tar xf ' + file_path + ' -C ' + added_folder_path)

    # start processing file
    machine_name = file_path[:-7]
    output = subprocess.check_output(['ls', '%s' % (machine_name)])
    kernel_list =  (output).splitlines()

    #FOR EACH KERNEL
    for kernel_path in kernel_list:
        kernel_name = kernel_path

        #UPLOAD TO KERNELVERSION DB
        kv, created_kv = KernelVersion.objects.get_or_create(name=kernel_name)
        kv.save
        kernel_path = machine_name + '/' + kernel_path + '/__pci_modules__'
        
        output = subprocess.check_output(['ls', '%s' % (kernel_path)])
        module_list = (output).splitlines()

        #FOR EACH MODULE IN THAT KERNEL VERSION
        for module_path in module_list:
            module_name = module_path
            module_path = kernel_path + '/' + module_path
            
            version_path = module_path + '/version'
            srcversion_path = module_path + '/srcversion'
            alias_path = module_path + '/aliases'

            version_name = 'null'
            srcversion_name = 'null'
            try:
                version_name = subprocess.check_output(['cat', '%s' % (version_path)])
            except subprocess.CalledProcessError:
                pass
            try:
                srcversion_name = subprocess.check_output(['cat', '%s' % (srcversion_path)])
            except subprocess.CalledProcessError:
                pass
            m, created_m = Module.objects.get_or_create(name=module_name, version=version_name, srcversion=srcversion_name)
            m.kernelVersions.add(kv)
            m.save

            output = subprocess.check_output( ['cat', '%s' % (alias_path)] )
            
            #FOR EACH ALIAS THAT CORRESPONDS TO THAT MODULE
            alias_list = (output.splitlines())
            for inst_alias in alias_list:
                alias_component = (inst_alias).rstrip('\\n').split(':')
                vendor = 'null'
                device = 'null'
                subvendor = 'null'
                subdevice = 'null'
                try:
                    if alias_component[0]:
                        vendor = alias_component[0]
                except:
                    pass
                try:
                    if alias_component[1]:
                        device = alias_component[1]
                except:
                    pass
                try:
                    if alias_component[2]:
                        subvendor = alias_component[2]
                except:
                    pass
                try:
                    if alias_component[3]:
                        subdevice = alias_component[3]
                except:
                    pass

                if vendor != 'null':
                    a, created_a = Aliases.objects.get_or_create(vendor=vendor, device=device, subvendor=subvendor, subdevice=subdevice)
                    a.module.add(m)
                    a.save

    os.system('rm -rf ' + file_path[:-7])
    KernelTarball.objects.get(tarToBeAdded=kernel_object.tarToBeAdded).delete()
