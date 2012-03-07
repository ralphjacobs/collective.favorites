from zope.component import getMultiAdapter

from plone.app.layout.viewlets.common import ViewletBase
from plone.uuid.interfaces import IUUID
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName

from .interfaces import IFavoriteStorage
from plone.app.layout.navigation.root import getNavigationRootObject


class SwitchFavorite(ViewletBase):

    index = ViewPageTemplateFile('switchfavorite.pt')

    def update(self):
        mtool = getToolByName(self.context, 'portal_membership')
        self.anonymous = mtool.isAnonymousUser()
        if self.anonymous:
            return

        user_id = mtool.getAuthenticatedMember().getId()
        super(SwitchFavorite, self).update()
        portal = getToolByName(self.context, 'portal_url').getPortalObject()
        site = getNavigationRootObject(self.context, portal)
        self.template = self.request.steps[-1]
        self.isfavorite = IFavoriteStorage(site).is_favorite(user_id,
                                                             IUUID(self.context))