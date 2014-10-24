from rest_framework import serializers

from schema.models import KernelVersion, Aliases
from pci_ids.models import pciam

class KernelVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = KernelVersion
        fields = ('name',)

class AliasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aliases
        fields = ('vendor', 'subvendor', 'device', 'subdevice', 'module')

class pci_idsSerializer(serializers.ModelSerializer):
	class Meta:
		model = pciam
		fields = ('val', 'v', 'd', 's')