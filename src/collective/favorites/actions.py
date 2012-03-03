from DateTime import DateTime

from Products.Five.browser import BrowserView

from .interfaces import IFavoriteStorage
from Products.CMFCore.utils import getToolByName
from Products.statusmessages.interfaces import IStatusMessage

from collective.favorites import FavoritesMessageFactory as _


class FavoriteActions(BrowserView):

    def add(self):
        request = self.request
        user = request.AUTHENTICATED_USER
        view = request.get('view', '')
        portal = getToolByName(self.context, 'portal_url').getPortalObject()
        IFavoriteStorage(portal).add_favorite(user.getId(),
                id=self.context.UID(),
                type='uid',
                view=view,
                date=DateTime())

        IStatusMessage(self.request).addStatusMessage(
                    _("The document has been added to your favorites"))
        self.request.response.redirect(self.context.absolute_url() + '/' + view)

    def remove(self):
        request = self.request
        user = request.AUTHENTICATED_USER
        view = request.get('view', '')
        portal = getToolByName(self.context, 'portal_url').getPortalObject()
        IFavoriteStorage(portal).remove_favorite(user.getId(),
                                                 id=self.context.UID())
        IStatusMessage(self.request).addStatusMessage(
                    _("The document has been removed from your favorites"))
        self.request.response.redirect(self.context.absolute_url() + '/' + view)