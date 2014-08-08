from django.test import TestCase
from django.test.client import Client

from schema.models import KernelVersion, Module, Aliases
from pci_ids.models import pciam

# Test for GetKernelVersions api call
class GetKernelVersionsTestCase(TestCase):
    def setUp(self):
        KernelVersion.objects.create(name="TestKernelVersion")
        KernelVersion.objects.create(name="TestKernelVersion2")
        KernelVersion.objects.create(name="TestKernelVersion3")
        self.c = Client()

    def testGetKernelVersions(self):
        response = self.c.get('/api/get_kernel_versions/', format='json')
        expectedResponse = '[{"name": "TestKernelVersion"}, {"name": "TestKernelVersion2"}, {"name": "TestKernelVersion3"}]'
        self.assertEquals(response.content, expectedResponse)

# Test for Diff api call
class DiffTestCase(TestCase):
    def setUp(self):
        self.testKernelVersion1 = KernelVersion.objects.create(name="TestKernelVersion1")
        self.testKernelVersion2 = KernelVersion.objects.create(name="TestKernelVersion2")

        self.testModuleOnlyKernel1 = Module.objects.create(name="TestModuleKernel1", version="1.0", srcversion="128E7DBE00BCDAD0108DE5A")
        self.testModuleOnlyKernel1.kernelVersions.add(self.testKernelVersion1)

        self.testModuleOnlyKernel2 = Module.objects.create(name="TestModuleKernel2", version="1.0", srcversion="23857DBE00BCDAD0108DE5A")
        self.testModuleOnlyKernel2.kernelVersions.add(self.testKernelVersion2)

        self.c = Client()

    def testDiffModules(self):
        # populate the schema with different module combinations
        testModuleBothKernels = Module.objects.create(name="TestModuleKernelBoth", version="1.0", srcversion="128E7DBE00BCDAD0108DE5A")
        testModuleBothKernels.kernelVersions.add(self.testKernelVersion1)
        testModuleBothKernels.kernelVersions.add(self.testKernelVersion2)
        testDiffModuleBothKernels = Module.objects.create(name="TestDiffModuleKernelBoth", version="1.0", srcversion="128E7DBE00BCDAD0108DE5A")
        testDiffModuleBothKernels.kernelVersions.add(self.testKernelVersion1)
        testDiffModuleBothKernels2 = Module.objects.create(name="TestDiffModuleKernelBoth", version="NULL", srcversion="NULL")
        testDiffModuleBothKernels2.kernelVersions.add(self.testKernelVersion2)
        # just a regular alias (with human-readable device mapping)
        testModuleOnlyKernel2Alias = Aliases.objects.create(vendor="9710", device="9815", subvendor = "1000", subdevice="0020")
        testModuleOnlyKernel2Alias.module.add(self.testModuleOnlyKernel2)
        response = self.c.get('/api/diff/'+self.testKernelVersion1.name+'/'+self.testKernelVersion2.name+'/', format='json')
        expectedResponse = '{"mods": [{"k1m": {"a": [], "srcv": "128E7DBE00BCDAD0108DE5A", "m": "TestDiffModuleKernelBoth", "kv": "TestKernelVersion1", "v": "1.0"}, "k2m": {"a": [], "srcv": "128E7DBE00BCDAD0108DE5A", "m": "TestDiffModuleKernelBoth", "kv": "TestKernelVersion2", "v": "1.0"}}, {"k1m": {"a": [], "srcv": "128E7DBE00BCDAD0108DE5A", "m": "TestModuleKernel1", "kv": "TestKernelVersion1", "v": "1.0"}, "k2m": null}, {"k1m": null, "k2m": {"a": [{"a": {"p": null, "r": "9710:9815:1000:0020"}}], "srcv": "23857DBE00BCDAD0108DE5A", "m": "TestModuleKernel2", "kv": "TestKernelVersion2", "v": "1.0"}}], "kv2m": 1, "kv1v": 0, "kv1m": 0, "kv2v": 0, "dv": 1}'
        self.assertEquals(response.content, expectedResponse)

    def testDiffAliases(self):
        pciam.objects.create(val="aa55", v="Ncomputing X300 PCI-Engine")
        pciam.objects.create(val="103c:323b:103c:3354", v="Hewlett-Packard Company", d="Smart Array Gen8 Controllers", s="P420i")
        # just a regular alias (with human-readable device mapping)
        testModuleOnlyKernel1Alias = Aliases.objects.create(vendor="9710", device="9815", subvendor = "1000", subdevice="0020")
        testModuleOnlyKernel1Alias.module.add(self.testModuleOnlyKernel1)
        # this one has that non-descriptive "1234" vendor
        testModuleOnlyKernel1Alias1234 = Aliases.objects.create(vendor="1234", device="9815", subvendor = "1000", subdevice="0020")
        testModuleOnlyKernel1Alias1234.module.add(self.testModuleOnlyKernel1)
        # this module only has vendor and device (and the device isn't valid)
        testModuleOnlyKernel1AliasVendorDevice = Aliases.objects.create(vendor="aa55", device="4x36")
        testModuleOnlyKernel1AliasVendorDevice.module.add(self.testModuleOnlyKernel1)
        # this module only has vendor and device (and neither is valid)
        testModuleOnlyKernel1AliasVendorDeviceNotExist = Aliases.objects.create(vendor="haha", device="4x36")
        testModuleOnlyKernel1AliasVendorDeviceNotExist.module.add(self.testModuleOnlyKernel1)
        # this module has the full alias to human-readable device map
        testModuleOnlyKernel1HasFullDeviceName = Aliases.objects.create(vendor="103c", device="323b", subvendor="103c", subdevice="3354")
        testModuleOnlyKernel1HasFullDeviceName.module.add(self.testModuleOnlyKernel1)
        response = self.c.get('/api/diff/'+self.testKernelVersion1.name+'/'+self.testKernelVersion2.name+'/', format='json')
        expectedResponse = '{"mods": [{"k1m": {"a": [{"a": {"p": "Ncomputing X300 PCI-Engine", "r": "aa55:4x36"}}, {"a": {"p": "Hewlett-Packard Company Smart Array Gen8 Controllers P420i", "r": "103c:323b:103c:3354"}}, {"a": {"p": null, "r": "9710:9815:1000:0020"}}, {"a": {"p": null, "r": "haha:4x36"}}, {"a": {"p": null, "r": "1234:9815:1000:0020"}}], "srcv": "128E7DBE00BCDAD0108DE5A", "m": "TestModuleKernel1", "kv": "TestKernelVersion1", "v": "1.0"}, "k2m": null}, {"k1m": null, "k2m": {"a": [], "srcv": "23857DBE00BCDAD0108DE5A", "m": "TestModuleKernel2", "kv": "TestKernelVersion2", "v": "1.0"}}], "kv2m": 0, "kv1v": 0, "kv1m": 5, "kv2v": 0, "dv": 0}'
        self.assertEquals(response.content, expectedResponse)

    def testDiffCounters(self):
        kernelModuleVersion1Counter = 1
        kernelModuleVersion2Counter = 2
        testDiffModuleBothKernels = Module.objects.create(name="TestDiffModuleKernelBoth", version="1.0", srcversion="128E7DBE00BCDAD0108DE5A")
        testDiffModuleBothKernels.kernelVersions.add(self.testKernelVersion1)
        testDiffModuleBothKernels2 = Module.objects.create(name="TestDiffModuleKernelBoth", version="NULL", srcversion="NULL")
        testDiffModuleBothKernels2.kernelVersions.add(self.testKernelVersion2)
        # just a regular alias (with human-readable device mapping)
        testModuleOnlyKernel1AliasForDiff = Aliases.objects.create(vendor="9710", device="9815", subvendor = "1000", subdevice="0020")
        testModuleOnlyKernel1AliasForDiff.module.add(testDiffModuleBothKernels)
        # just a regular alias (with human-readable device mapping)
        testModuleOnlyKernel2AliasForDiff = Aliases.objects.create(vendor="9710", device="9835", subvendor = "1000", subdevice="0020")
        testModuleOnlyKernel2AliasForDiff.module.add(testDiffModuleBothKernels2)
        # just a regular alias (with human-readable device mapping)
        testModuleOnlyKernel2AliasForDiff2 = Aliases.objects.create(vendor="9710", device="9815")
        testModuleOnlyKernel2AliasForDiff2.module.add(testDiffModuleBothKernels2)
        response = self.c.get('/api/diff/'+self.testKernelVersion1.name+'/'+self.testKernelVersion2.name+'/', format='json')
        expectedResponse = '{"mods": [{"k1m": {"a": [{"a": {"p": null, "r": "9710:9815:1000:0020"}}], "srcv": "128E7DBE00BCDAD0108DE5A", "m": "TestDiffModuleKernelBoth", "kv": "TestKernelVersion1", "v": "1.0"}, "k2m": {"a": [{"a": {"p": null, "r": "9710:9815"}}, {"a": {"p": null, "r": "9710:9835:1000:0020"}}], "srcv": "128E7DBE00BCDAD0108DE5A", "m": "TestDiffModuleKernelBoth", "kv": "TestKernelVersion2", "v": "1.0"}}, {"k1m": {"a": [], "srcv": "128E7DBE00BCDAD0108DE5A", "m": "TestModuleKernel1", "kv": "TestKernelVersion1", "v": "1.0"}, "k2m": null}, {"k1m": null, "k2m": {"a": [], "srcv": "23857DBE00BCDAD0108DE5A", "m": "TestModuleKernel2", "kv": "TestKernelVersion2", "v": "1.0"}}], "kv2m": 0, "kv1v": 1, "kv1m": 0, "kv2v": 2, "dv": 1}'
        self.assertEquals(response.content, expectedResponse)