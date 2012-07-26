from BTrees.OOBTree import OOBTree
from persistent.dict import PersistentDict
from persistent.list import PersistentList

from zope.interface import implements
from zope.component import adapts
from zope.annotation.interfaces import IAnnotations

from plone.app.layout.navigation.interfaces import INavigationRoot

from .interfaces import IFavoriteStorage


FAVORITE_KEY = 'collective.favorites'

class FavoriteStorage(object):

    adapts(INavigationRoot)
    implements(IFavoriteStorage)

    def __init__(self, context):
        self.annotations = IAnnotations(context)

    def get_favorites(self):
        if not FAVORITE_KEY in self.annotations:
            self.annotations[FAVORITE_KEY] = OOBTree()

        return self.annotations[FAVORITE_KEY]

    def add_favorite(self, userid, id, type, **kwargs):
        value = PersistentDict(type=type,
                               id=id,
                               **kwargs)

        if self.is_favorite(userid, id):
            self.remove_favorite(userid, type, id)

        if not userid in self.get_favorites():
            self.annotations[FAVORITE_KEY][userid] = PersistentList()

        self.annotations[FAVORITE_KEY][userid].append(value)

    def remove_favorite(self, userid, id):
        favorites_list = self.get_favorites()[userid]
        for num, value in enumerate(favorites_list):
            if value['id'] == id:
                break
        else:
            raise KeyError, "No value for %s in %s favorites" % (id, userid)

        favorites_list.remove(favorites_list[num])
        self.annotations[FAVORITE_KEY][userid] = favorites_list

    def is_favorite(self, userid, id):
        if not userid in self.get_favorites():
            return False

        favorites_list = self.annotations[FAVORITE_KEY][userid]
        for num, value in enumerate(favorites_list):
            if value['id'] == id:
                return True
        else:
            return False

    def list_favorites(self, userid):
        return list(self.get_favorites().get(userid, []))