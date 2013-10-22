import os
import sys

from datetime import datetime
import settings
import urllib
import urllib2


class Handler(object):
    def __init__(self, f):
        self.file = f

    def get_temp_folder_name(self):
        return str(datetime.now()).replace(' ', '_').replace(':', '-').replace('.', '_')

    def get_temp_folder_path(self):
        return os.path.join(
            settings.TEMP_UNPACK_PATH,
            self.get_temp_folder_name()
        )

    def create_target_path(self, target_path):
        print 'making target path', target_path
        try:
            os.makedirs(target_path)
        except OSError:
            # Path probaly exists
            pass

    #perform basic stuff
    def execute(self):
        self.create_target_path(self.file.get_pretty_path())

    def post_execute(self):
        pass
