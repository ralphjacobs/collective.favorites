from datetime import datetime

from Products.Five.browser import BrowserView

from plone.uuid.interfaces import IUUID
from Products.CMFCore.utils import getToolByName
from Products.statusmessages.interfaces import IStatusMessage

from collective.favorites import FavoritesMessageFactory as _
from .interfaces import IFavoriteStorage
from plone.app.layout.navigation.root import getNavigationRootObject


class FavoriteActions(BrowserView):

    def add(self):
        request = self.request
        user = request.AUTHENTICATED_USER
        view = request.get('view', '')
        portal = getToolByName(self.context, 'portal_url').getPortalObject()
        site = getNavigationRootObject(self.context, portal)
        IFavoriteStorage(site).add_favorite(user.getId(),
                id=IUUID(self.context),
                type='uid',
                view=view,
                date=datetime.now())

        IStatusMessage(self.request).addStatusMessage(
                    _("The document has been added to your favorites"))
        self.request.response.redirect(self.context.absolute_url() + '/' + view)

    def remove(self):
        request = self.request
        user = request.AUTHENTICATED_USER
        view = request.get('view', '')
        portal = getToolByName(self.context, 'portal_url').getPortalObject()
        site = getNavigationRootObject(self.context, portal)
        IFavoriteStorage(site).remove_favorite(user.getId(),
                                                 id=IUUID(self.context))
        IStatusMessage(self.request).addStatusMessage(
                    _("The document has been removed from your favorites"))
        self.request.response.redirect(self.context.absolute_url() + '/' + view)