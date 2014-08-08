from django.test import TestCase
from django.db import IntegrityError

from schema.models import KernelVersion, Module, Aliases

# Tests for the schema_kernel models
class SchemaModelsTestCase(TestCase):
    def setUp(self):
        testKernelVersion = KernelVersion.objects.create(name="TestKernelVersion")
        testModule = Module.objects.create(name="TestModule", version="1.0", srcversion="128E7DBE00BCDAD0108DE5A")
        testModule.kernelVersions.add(testKernelVersion)
        testAlias = Aliases.objects.create(vendor="1234", device="5678", subvendor="912", subdevice="null")
        testAlias.module.add(testModule)

    def testDuplicateModules(self):
        errorOccured = False
        try:
            duplicateModule = Module.objects.create(name="TestModule", version="1.0", srcversion="128E7DBE00BCDAD0108DE5A")
        except IntegrityError:
            errorOccured = True

        self.assertTrue(errorOccured)

    def testDuplicateModuleNameForKernelVersion(self):
        errorOccured = False
        try:
            originalKernelVersion = KernelVersion.objects.get(name="TestKernelVersion")
            duplicateModule = Module.objects.create(name="TestModule", version="2.0", srcversion="128E7DBE00BCDAD0108DE5B")
            duplicateModule.save
            duplicateModule.kernelVersions.add(originalKernelVersion)
        except IntegrityError:
            errorOccured = True
        self.assertTrue(errorOccured)

    def testUnicodeModule(self):
        testModule = Module.objects.create(name="TestModule", version="1.0", srcversion="NULL")
        self.assertEquals(testModule.__unicode__(), u"TestModule 1.0")
        testModule2 = Module.objects.create(name="TestModule", version="2.0", srcversion="128E7DBE00BCDAD0108DE5B")
        self.assertEquals(testModule2.__unicode__(), u"TestModule 2.0 128E7DBE00BCDAD0108DE5B")

    def testDuplicateAliasesWithNulls(self):
        errorOccured = False
        try:
            testAlias1 = Aliases.objects.create(vendor="1234", device="5678", subvendor="null", subdevice="null")
            testAlias2 = Aliases.objects.create(vendor="1234", device="5678", subvendor="null", subdevice="null")
        except IntegrityError:
            errorOccured = True
        self.assertTrue(errorOccured)

    def testUnicodeAlias(self):
        testAlias = Aliases.objects.get(vendor="1234", device="5678", subvendor="912", subdevice="null")
        self.assertEquals(testAlias.__unicode__(), u"1234:5678:0912")
        testAlias2 = Aliases.objects.create(vendor="1234", device="5678", subvendor="9128", subdevice="0000")
        self.assertEquals(testAlias2.__unicode__(), u"1234:5678:9128:0000")