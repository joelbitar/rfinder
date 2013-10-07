import re

import settings
from analyzer import Analyzer

from mutagen.easyid3 import EasyID3

class MusicFileMetadataReader(object):
    def get_file_type(self):
        return self.file.full_path.split('.')[-1].lower()
    
    def __init__(self, file):
        self.file = file

    def get_from_mp3(self):
        id3_file = EasyID3(self.file.full_path)
        meta_data = {
            'album' : None,
            'artist' : None
        }

        if id3_file.get('artist'):
            meta_data['artist'] = id3_file.get('artist')[0]
        
        if id3_file.get('album'):
            meta_data['album'] = id3_file.get('album')[0]

        return meta_data

    def get_metadata(self):
        return {
            'mp3' : self.get_from_mp3
        }.get(self.get_file_type())()

    def get_artist(self):
        return self.get_metadata().get('artist', None)

    def get_album(self):
        return self.get_metadata().get('album', None)

class MusicAnalyzer(Analyzer):
    patterns_and_confidence = [
        (r'.*[\d]CD.*', 40),
        (r'.*\.mp3$', 90),
    ]

    def get_confidence(self):
        # Now.. for the fun part!
        confidences = [0]

        for path_part in self.file.get_path_parts():
            for regexp, confidence in self.patterns_and_confidence:
                if re.match(regexp, path_part):
                    confidences.append(confidence)

        return max(confidences)

    def get_artist_and_album_name(self):
        artist = ""
        album = ""

        for path_part in reversed(self.file.get_path_parts()):
            splitted = path_part.split('-')
            if len(splitted) > 1:
                artist = splitted[0]
                album = splitted[1]

        # IF we didn't find anything, use the first part of the path.
        if not artist:
            artist = self.file.get_path_parts()[0]

        # Assume that we get better data from the tagreader
        tag_reader = MusicFileMetadataReader(self.file)
        try:
            if tag_reader.get_artist():
                artist = tag_reader.get_artist()
        except :
            pass

        try:
            if tag_reader.get_album():
                album = tag_reader.get_album()
        except :
            pass
        
        return {
            'artist' : self.get_cleaned_name(artist.replace("_", ' ')),
            'album' : self.get_cleaned_name(album.replace("_", ' '))
        }

    def get_artist_name(self):
        return self.get_artist_and_album_name()['artist']


    def get_album_name(self):
        return self.get_artist_and_album_name()['album']


    def get_pretty_path_list(self):
        return [self.get_artist_name(), self.get_album_name()]

    def get_pretty_path(self):
        pretty_path = self.get_absolut_path(
           [settings.FOLDERS_MUSIC] + self.get_pretty_path_list()
        )

        if settings.VERBOSE > 1:
            print 'MusicAnalyzer.get_pretty_path()'
            print 'Pretty path: %s' % (pretty_path)
            print [settings.FOLDERS_MUSIC] + self.get_pretty_path_list()

        return pretty_path

