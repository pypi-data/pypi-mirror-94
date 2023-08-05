# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from library.policy.testing import LIBRARY_POLICY_INTEGRATION_TESTING  # noqa
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from Products.CMFPlone.utils import get_installer

import unittest


class TestSetup(unittest.TestCase):
    """Test that library.policy is properly installed."""

    layer = LIBRARY_POLICY_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        self.installer = get_installer(self.portal, self.layer["request"])

    def test_product_installed(self):
        """Test if library.policy is installed."""
        self.assertTrue(self.installer.isProductInstalled("library.policy"))

    def test_browserlayer(self):
        """Test that ILibraryPolicyLayer is registered."""
        from library.policy.interfaces import ILibraryPolicyLayer
        from plone.browserlayer import utils

        self.assertIn(ILibraryPolicyLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = LIBRARY_POLICY_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.installer = get_installer(self.portal, self.layer["request"])
        roles_before = api.user.get_roles(TEST_USER_ID)
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.installer.uninstallProducts(["library.policy"])
        setRoles(self.portal, TEST_USER_ID, roles_before)

    def test_product_uninstalled(self):
        """Test if library.policy is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled("library.policy"))

    def test_browserlayer_removed(self):
        """Test that ILibraryPolicyLayer is removed."""
        from library.policy.interfaces import ILibraryPolicyLayer
        from plone.browserlayer import utils

        self.assertNotIn(ILibraryPolicyLayer, utils.registered_layers())
