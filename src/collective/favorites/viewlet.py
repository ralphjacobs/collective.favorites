from zope.component import getMultiAdapter

from plone.app.layout.viewlets.common import ViewletBase
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName

from .interfaces import IFavoriteStorage

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
        self.template = self.request.steps[-1]
        self.isfavorite = IFavoriteStorage(portal).is_favorite(user_id, self.context.UID())