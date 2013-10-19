__author__ = 'joel'

class Torrent(object):
    __json = None
    __torrent_hash = None

    JSON_MAP = {
        'name': 4,
        'size': 5,
        'downloaded': 8,
        'path': 25
    }

    def __init__(self, torrent_hash, json):
        self.__json = json
        self.__torrent_hash = torrent_hash

    def __getattr__(self, item):
        return self.json[self.JSON_MAP.get(item)]

    @property
    def json(self):
        return self.__json

    @property
    def id(self):
        return self.__torrent_hash

    @property
    def is_done(self):
        #self.legend()
        #print 'size', self.size
        #print 'downloaded', self.downloaded
        return self.size == self.downloaded

    def legend(self):
        for idx, item in enumerate(self.json):
            print idx, item

    def __str__(self):
        return '{name}'.format(
            name=self.name
        )
