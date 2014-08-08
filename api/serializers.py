from rest_framework import serializers

from schema.models import KernelVersion, Aliases

class KernelVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = KernelVersion
        fields = ('name',)

class AliasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aliases
        fields = ('vendor', 'subvendor', 'device', 'subdevice', 'module')