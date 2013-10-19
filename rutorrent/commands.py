__author__ = 'joel'
from simplejson import loads
from torrent import Torrent
import requests
from requests.auth import HTTPBasicAuth

class ruTorrentCommand(object):
    __path = None
    __post_data = None
    __ru_torrent_instance = None

    def __init__(self, path, post_data):
        self.__path = path
        self.__post_data = post_data

    @property
    def path(self):
        return self.__path

    @property
    def url(self):
        return "{base_url}/{path}".format(
            base_url=self.ru_torrent_instance.url.rstrip('/'),
            path=self.path.lstrip('/')
        )

    @property
    def post_data(self):
        return self.__post_data

    def set_ru_torrent_instance(self, ru_torrent_instance):
        self.__ru_torrent_instance=ru_torrent_instance

    @property
    def ru_torrent_instance(self):
        return self.__ru_torrent_instance

    def get_basic_auth(self):
        if not self.ru_torrent_instance.basic_auth:
            return None

        return HTTPBasicAuth(
            username=self.ru_torrent_instance.basic_auth.get('username'),
            password=self.ru_torrent_instance.basic_auth.get('password'),
        )

    def perform_post(self):
        print 'headers', self.ru_torrent_instance.headers
        print 'Auth:', self.get_basic_auth()

        response = requests.post(
            self.url,
            data=self.post_data,
            headers=self.ru_torrent_instance.headers,
            verify=self.ru_torrent_instance.verify_ssl_certificate,
            auth=self.get_basic_auth()
        )

        return response

    def get_json_response(self):
        """
        s = '{"t":{"E4060C0EEDDE9EF0E0B0E8D8DDB62B8F62336F44":["1","0","1","1","Christopher.Walken.MOViE.PACK.1080p.BluRay.x264-SCC","296644621293","35363","35363","296644621293","0","0","0","0","8388608","","1","79","1","0","0","2","1382152880","10034921606","0","35363","\/home\/joel/projects/rfinder/seedbox\/torrents\/data\/Christopher.Walken.MOViE.PACK.1080p.BluRay.x264-SCC","1381269264","1","1","","","2582225178624","1","1","","","","","52#","49#","","",""],"2E84CC87B6EA1FF49FF0199B1E55EB3F342218A8":["1","0","1","0","Homeland.S03E03.720p.HDTV.x264-IMMERSE","1476192006","2816","2816","1476192006","0","0","0","0","524288","","0","8","0","0","0","2","1382171315","221954789","0","2816","\/home\/joel/projects/rfinder/seedbox\/torrents\/data\/Homeland.S03E03.720p.HDTV.x264-IMMERSE","1381740472","1","0","","","2582225178624","1","1","","","","","215#","11#","","1382165569\n","1382165495\n"]},"cid":464607101}'
        s = s.replace('\n','')
        return loads(s)['t']
        """
        r = self.perform_post()

        return r.json()['t']


class ruTorrentGetTorrentListCommand(ruTorrentCommand):
    def get_torrents(self):
        r = self.get_json_response()
        print len(r)
        for key, torrent_data in r.items():
            yield Torrent(key, torrent_data)

        return

    def __iter__(self):
        for t in self.get_torrents():
            yield t

        return


class ruTorrentCommands(object):
    __ru_torrent_instance = None
    def __init__(self, ru_torrent_instance):
        self.__ru_torrent_instance = ru_torrent_instance

    @property
    def ru_torrent_instance(self):
        return self.__ru_torrent_instance

    def get_torrent_list(self):
        c =  ruTorrentGetTorrentListCommand(
            path='plugins/httprpc/action.php',
            post_data='mode=list&cid=229885160&cmd=d.get_throttle_name%3D&cmd=d.get_custom%3Dchk-state&cmd=d.get_custom%3Dchk-time&cmd=d.get_custom%3Dsch_ignore&cmd=cat%3D%22%24t.multicall%3Dd.get_hash%3D%2Ct.get_scrape_complete%3D%2Ccat%3D%7B%23%7D%22&cmd=cat%3D%22%24t.multicall%3Dd.get_hash%3D%2Ct.get_scrape_incomplete%3D%2Ccat%3D%7B%23%7D%22&cmd=cat%3D%24d.views%3D&cmd=d.get_custom%3Dseedingtime&cmd=d.get_custom%3Daddtime'
        )
        c.set_ru_torrent_instance(
            self.ru_torrent_instance
        )
        return c

