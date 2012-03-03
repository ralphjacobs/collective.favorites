from collective.favorites.interfaces import IFavoritesPolicy
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import normalizeString

class UIDPolicy(object):

    def get_favorites_infos(self, context, favorites_list):
        """Return content infos
        """
        favorites_dict = dict([(f['id'], f) for f in favorites_list])
        ctool = getToolByName(context, 'portal_catalog')
        portal_url = getToolByName(context, 'portal_url')()
        brains = ctool.unrestrictedSearchResults(UID=[f['id'] for f in favorites_list])

        infos = []
        for brain in brains:
            uid = brain.UID
            icon_url = brain.getIcon and "%s/%s" % (portal_url, brain.getIcon) or None
            info = {'url': brain.getURL() + '/' + favorites_dict[uid].get('view', ''),
                    'description': brain.Description,
                    'title': brain.Title,
                    'icon': icon_url,
                    'class': 'contenttype-%s' % brain.portal_type.lower(),
                    'index': '%s-%s' % (brain.portal_type,
                                        normalizeString(brain.Title,
                                                        context=context))
                    }
            infos.append(info)

        return infos
