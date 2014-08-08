import requests, json, ast

from mysite import settings

from django.http import HttpResponseRedirect
from django.shortcuts import render

from cert.forms import DeviceEnablementForm

from schema.models import Module, KernelVersion

# Create your views here.
def cert(request):
    # this sets the correct url root for making api requests
    if settings.ON_PAAS:
        api_url_root = 'http://vermanlab-jmitchel.rhcloud.com'
    else:
        api_url_root = 'http://localhost:8000'

    # this gets all the possible hardware aliases so the user can select from the form
    get_hardware_enablement_list_url = api_url_root + '/api/get_devices'
    aliases = json.loads(requests.get(get_hardware_enablement_list_url, params=request.GET).text)

    enabled_kernels = []
    nonenabled_kernels = []

    # render the form (and the enabled/non-enabled kernels if the user has selected an alias)
    if request.method == 'POST':
        form = DeviceEnablementForm(request.POST, alias_list = aliases)
        if form.is_valid():
            #selectedAlias is the selected alias
            selectedAlias = form.cleaned_data['selectedAlias']
            aliasDict = ast.literal_eval(selectedAlias)

            for mod in aliasDict['module']:
                realMod = Module.objects.get(pk=mod)
                kernelVersions = realMod.kernelVersions.all()
                for kv in kernelVersions:
                    if kv not in enabled_kernels and kv.errata:
                        enabled_kernels.append(kv)

            for kernel in KernelVersion.objects.all():
                if kernel not in enabled_kernels and kernel.errata:
                    nonenabled_kernels.append(kernel)

        enabled_kernels.sort(key=lambda x: x.errata, reverse=False)
        nonenabled_kernels.sort(key=lambda x: x.errata, reverse=False)
    else:
        form = DeviceEnablementForm(alias_list = aliases)

    return render(request, 'cert/cert.html', {
        'form': form,
        'enabled_kernels': enabled_kernels,
        'nonenabled_kernels': nonenabled_kernels,
    })