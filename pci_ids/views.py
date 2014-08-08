import urllib2

from django.shortcuts import render
from django.db import IntegrityError
from django.http import HttpResponse
from django.views.generic import View

from pci_ids.models import pciam

class pci_ids(View):
    def parse_pci_ids_file(self, pci_ids_file):
        tab_level = 0

        final_list = ""

        vendor = ""
        device = ""
        subs = ""

        vendor_pretty = ""
        device_pretty = ""
        subs_pretty = ""

        for line in pci_ids_file:
            # substyle aliases
            if line.startswith('\t\t'):
                subs = line[2:11].replace(' ', ':')
                subs_pretty = line[13:-1]
                value = vendor + ":" + device + ":" + subs
                if pciam.objects.filter(v=vendor_pretty, d=device_pretty, s=subs_pretty).count() == 0:
                    if not vendor.startswith('#'):
                        a, created_a = pciam.objects.get_or_create(val=value, v=vendor_pretty, d=device_pretty, s=subs_pretty)
                        a.save
            # device style aliases
            elif line.startswith('\t'):
                device = line[1:5]
                device_pretty = line[7:-1]
                value = vendor + ":" + device
                if pciam.objects.filter(v=vendor_pretty, d=device_pretty).count() == 0:
                    if not vendor.startswith('#'):
                        a, created_a = pciam.objects.get_or_create(val=value, v=vendor_pretty, d=device_pretty)
                        a.save
            # possibly vendor style aliases
            else:
                # this is the end of the vendor, devices, subvendor, subdevice style aliases in the pci.ids document
                if line.startswith("# C class"):
                    break
                vendor = line[0:4]
                vendor_pretty = line[6:-1]
                device = ""
                device_pretty = ""
                subs = ""
                subs_pretty = ""
                value = vendor
                # if it's a comment don't add to DB
                if not vendor.startswith('#'):
                    try:
                        a, created_a = pciam.objects.get_or_create(val=value, v=vendor_pretty)
                    except IntegrityError:
                        pass

    # this method puls the pci.ids file using urllib2 and then parses that file and adds everything to the pci_ids pciam table
    def add_pci_ids_file(self):
        url = 'http://pciids.sourceforge.net/v2.2/pci.ids'
        response = urllib2.urlopen(url) 
        self.parse_pci_ids_file(response.readlines())

    def get(self, request):
        self.add_pci_ids_file()
        # Redirect to the document list after POST
        return HttpResponse("pci.ids file uploaded to verman lab database.")
