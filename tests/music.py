import os
import sys
from datetime import datetime
from unittest import TestCase

import tests
import settings
from files import files
import pyunrar

from analyzer.show import ShowAnalyzer
from analyzer.movie import MovieAnalyzer

from models import directory

class MusicTests(TestCase):
    def setUp(self):
        self.base_path = os.path.join(os.getcwd(), 'mock_downloads_dir')

        files.removeall(self.base_path)

        rarfile =  pyunrar.RarFile(os.path.join(os.getcwd(), 'mock_downloads_dir.rar'))
        rarfile.extract(os.getcwd())

        settings.DOWNLOADS_FOLDER = self.base_path
        settings.FOLDERS_MOVIES = os.path.join(os.getcwd(), 'target_folder', 'movies')
        settings.FOLDERS_TV_SHOWS = os.path.join(os.getcwd(), 'target_folder', 'shows')

        settings.VERBOSE = True

        files.removeall(settings.FOLDERS_MOVIES)
        files.removeall(settings.FOLDERS_TV_SHOWS)


    def tearDown(self):
        files.removeall(self.base_path)
        os.rmdir(self.base_path)


    def test_should_get_artist_folder(self):
        for path in files.find_all_files(os.path.join(self.base_path, 'Radiohead-The_King_Of_Limbs-(Retail)-2012-CR')):
            path_parts = path.get_handler().file.get_path_parts()
            if path.is_interesting():
                path.get_handler().file.get_pretty_path()


    def test_get_normal_names(self):
        for path in files.find_all_files(os.path.join(self.base_path, 'Simon_And_Garfunkel-Bridge_Over_Troubled_Water-(40th Anniversary_Edition)-2CD-2011-C4')):
            path_parts = path.get_handler().file.get_path_parts()
            print path_parts
            file = path.get_handler().file

            print file.get_analyzer()

            print "pretty path", file.get_pretty_path()

    def test_extract_from_id3(self):
        name = 'Freestylers - Pressure Point'
        for path in files.find_all_files(os.path.join(self.base_path, name)):
            path_parts = path.get_handler().file.get_path_parts()

            file_handler = path.get_handler().file
            
            if path.is_interesting():
                self.failUnlessEqual(
                    path.get_handler().file.get_pretty_path(),
                    os.path.join('/media/arnie/media/music', 'Freestylers', 'Pressure Point') + '/'
                )


