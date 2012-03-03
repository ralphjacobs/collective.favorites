import unittest2 as unittest

from DateTime import DateTime

from Products.CMFCore.utils import getToolByName

from collective.favorites.testing import\
    COLLECTIVE_FAVORITES_INTEGRATION_TESTING

from collective.favorites.interfaces import IFavoriteStorage

class TestExample(unittest.TestCase):

    layer = COLLECTIVE_FAVORITES_INTEGRATION_TESTING

    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']
        self.qi_tool = getToolByName(self.portal, 'portal_quickinstaller')

    def test_product_is_installed(self):
        """ Validate that our products GS profile has been run and the product
            installed
        """
        pid = 'collective.favorites'
        installed = [p['id'] for p in self.qi_tool.listInstalledProducts()]
        self.assertTrue(pid in installed,
                        'package appears not to have been installed')

    def test_favorite_storage(self):
        storage = IFavoriteStorage(self.portal)
        storage.add_favorite('toto', 'uid', self.portal.Members.UID(), DateTime())
        storage.add_favorite('toto', 'uid', self.folder.UID(), DateTime())
        self.assertEqual(len(storage.get_favorites()), 2)
        storage.remove_favorite('toto', self.folder.UID())
        self.assertEqual(len(storage.get_favorites()), 1)

    def test_favorite_actions(self):
        self.portal.Members.restrictedTraverse('@@add-favorite')()
        storage = IFavoriteStorage(self.portal)
        self.assertEqual(len(storage.get_favorites()), 1)

        self.portal.Members.restrictedTraverse('@@remove-favorite')()
        self.assertEqual(len(storage.get_favorites()), 0)