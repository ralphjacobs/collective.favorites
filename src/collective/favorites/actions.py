from datetime import datetime

from Products.Five.browser import BrowserView

from plone.uuid.interfaces import IUUID
from Products.CMFCore.utils import getToolByName
from Products.statusmessages.interfaces import IStatusMessage

from collective.favorites import FavoritesMessageFactory as _
from .interfaces import IFavoriteStorage
from plone.app.layout.navigation.root import getNavigationRootObject
from Products.CMFCore.interfaces._content import IFolderish


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

        statusmsg = IStatusMessage(request)
        if IFolderish.providedBy(self.context):
            statusmsg.add(_("The folder has been added to your favorites"))
        else:
            statusmsg.add(_("The document has been added to your favorites"))

        request.response.redirect(self.context.absolute_url() + '/' + view)

    def remove(self):
        request = self.request
        user = request.AUTHENTICATED_USER
        view = request.get('view', '')
        portal = getToolByName(self.context, 'portal_url').getPortalObject()
        site = getNavigationRootObject(self.context, portal)
        IFavoriteStorage(site).remove_favorite(user.getId(),
                                                 id=IUUID(self.context))


        statusmsg = IStatusMessage(request)
        if IFolderish.providedBy(self.context):
            statusmsg.add(_("The folder has been removed from your favorites"))
        else:
            statusmsg.add(_("The document has been removed from your favorites"))

        request.response.redirect(self.context.absolute_url() + '/' + view)