from plone.i18n.normalizer.interfaces import IIDNormalizer
from plone.memoize.instance import memoize
from plone.portlets.interfaces import IPortletDataProvider
from zope.component import getMultiAdapter, queryUtility, getUtilitiesFor
from zope.formlib import form
from zope.interface import implements

from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from plone.app.portlets.portlets import base

from collective.favorites import FavoritesMessageFactory as _
from collective.favorites.interfaces import IFavoriteStorage, IFavoritesPolicy
from plone.app.layout.navigation.root import getNavigationRootObject


class IFavoritesPortlet(IPortletDataProvider):

    pass


class Assignment(base.Assignment):
    implements(IFavoritesPortlet)

    @property
    def title(self):
        return _(u"Favorites List")


class Renderer(base.Renderer):

    render = ViewPageTemplateFile('favorites.pt')

    title = _("Favorites")

    @property
    def anonymous(self):
        context = aq_inner(self.context)
        portal_state = getMultiAdapter((context, self.request),
                                       name=u'plone_portal_state')
        return portal_state.anonymous()

    @property
    def available(self):
        return not self.anonymous and len(self._data())

    def favorites_items(self):
        return self._data()

    @memoize
    def _data(self):
        policies = getUtilitiesFor(IFavoritesPolicy)
        mtool = getToolByName(self.context, 'portal_membership')
        user_id = mtool.getAuthenticatedMember().getId()
        portal = getToolByName(self.context, 'portal_url').getPortalObject()
        site = getNavigationRootObject(self.context, portal)
        favorites_list = IFavoriteStorage(site).list_favorites(user_id)

        favorites_infos = []
        for policy_name, policy in policies:
            favorites_infos.extend(policy.get_favorites_infos(self.context,
                    [fav for fav in favorites_list if fav['type'] == policy_name]))

        favorites_infos.sort(key=lambda x: x['index'])
        return favorites_infos


class AddForm(base.NullAddForm):
    form_fields = form.Fields(IFavoritesPortlet)
    label = _(u"Add Favorites Portlet")
    description = _(u"This portlet displays the documents you have selected as your favorites.")

    def create(self):
        return Assignment()