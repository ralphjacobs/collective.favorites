from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting
from plone.app.testing import applyProfile

from zope.configuration import xmlconfig

class CollectiveFavorites(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE, )

    def setUpZope(self, app, configurationContext):
        # Load ZCML for this package
        import collective.favorites
        xmlconfig.file('configure.zcml',
                       collective.favorites,
                       context=configurationContext)


    def setUpPloneSite(self, portal):
        applyProfile(portal, 'collective.favorites:default')

COLLECTIVE_FAVORITES_FIXTURE = CollectiveFavorites()
COLLECTIVE_FAVORITES_INTEGRATION_TESTING = \
    IntegrationTesting(bases=(COLLECTIVE_FAVORITES_FIXTURE, ),
                       name="CollectiveFavorites:Integration")