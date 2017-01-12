#!/usr/bin/env python

##############################################################################
#
# Copyright (C) Zenoss, Inc. 2015, all rights reserved.
#
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
#
##############################################################################

"""
    "usePowershell" datasource option ignored in zenpacklib created ZenPacks (ZEN-25315)
"""
# Zenoss Imports
import Globals  # noqa
from Products.ZenUtils.Utils import unused
unused(Globals)


# stdlib Imports
from Products.ZenTestCase.BaseTestCase import BaseTestCase

# zenpacklib Imports
from ZenPacks.zenoss.ZenPackLib.tests.ZPLTestHarness import ZPLTestHarness


YAML_DOC = """
name: ZenPacks.zenoss.Microsoft.Windows

device_classes:
  /Server/Microsoft:
    templates:
      TestTemplate:
        description: This is a test to show usePowershell setting not working
        datasources:
          usePowershellDatasource:
            type: Windows Shell 
            strategy: Custom Command 
            cycletime: 300
            eventClass: /Status
            enabled: true
            usePowershell: false
            script: 'dir'
            parser: Auto
"""


class TestUsePowershellDatasource(BaseTestCase):
    """
    "usePowershell" datasource option ignored in zenpacklib created ZenPacks (ZEN-25315)
    """

    def test_datasource_boolean(self):
        z = ZPLTestHarness(YAML_DOC)
        if z.zenpack_installed():
            z.connect()
            # check properties on dummy template
            dcs = z.cfg.device_classes.get('/Server/Microsoft')
            tcs = dcs.templates.get('TestTemplate')
            t = tcs.create(z.dmd, False)
            ds = t.datasources()[0]

            self.assertTrue(isinstance(ds.usePowershell, bool),
                    'Datasource property (usePowershell) should be bool, got {}'.format(type(ds.usePowershell)))
            self.assertEquals(ds.usePowershell, False,
                    'Datasource property (usePowershell) should be False, got {}'.format(ds.usePowershell))
        else:
            print '\nSkipping test_integer_threshold since ZenPacks.zenoss.Microsoft.Windows not installed.'


def test_suite():
    """Return test suite for this module."""
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestUsePowershellDatasource))
    return suite

if __name__ == "__main__":
    from zope.testrunner.runner import Runner
    runner = Runner(found_suites=[test_suite()])
    runner.run()
