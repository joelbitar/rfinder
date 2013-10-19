__author__ = 'joel'

from commands import ruTorrentCommands
from tracker.tracker import Tracker


class ruTorrent(object):
    __url = None
    __headers = None
    __basic_auth = None
    __commands = None
    __verify_ssl_certificate = False

    def __init__(self, url):
        self.__url = url
        self.__commands = ruTorrentCommands(
            ru_torrent_instance=self
        )
        self.__headers = {}

    def set_basic_auth_hash(self, s):
        user_pass = s.split(':')
        self.__basic_auth = {
            'username': user_pass[0],
            'password': user_pass[1]
        }
        #self.__headers['Authentication'] = "Basic: {key}=".format(key=s);

    @property
    def basic_auth(self):
        return self.__basic_auth

    @property
    def verify_ssl_certificate(self):
        return self.__verify_ssl_certificate

    @property
    def url(self):
        return self.__url

    @property
    def headers(self):
        if not self.__headers:
            return []

        return self.__headers


    @property
    def commands(self):
        return self.__commands
