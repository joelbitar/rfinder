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

class ExtractCleanName(TestCase):
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


    def test_remove_watermarks(self):
        s = "Toddlers.and.Tiaras.S03E01.Le.Maison.de.Paris.HDTV.XviD-MOMENTUM [NO-RAR] - [ www.torrentday.com ]"

        paths = files.find_all_files(os.path.join(self.base_path, s))
        path = [p for p in paths][0]

        pretty_path = path.get_handler().file.get_pretty_path()

        self.failUnless(1 > pretty_path.find("torrentday"), pretty_path)
        self.failUnless(1 > pretty_path.lower().find("NO-RAR"))
    
    def test_should_extract_path_parts(self):
        paths = files.find_all_files(os.path.join(self.base_path, 'Some.Movie.Archive'))
        paths = [p for p in paths]

        path = paths[0]
        path_parts = path.get_handler().file.get_path_parts()

        self.failUnlessEqual(3, len(path_parts), "Was NOT three")
        self.failUnlessEqual(
            ['Some.Random.Movie.Sequel', 'mapsm2.avi', 'Some.Movie.Archive'],
            path_parts,
            path_parts
        )

        pretty_path = path.get_handler().file.get_pretty_path()

        self.failUnless(pretty_path.startswith(settings.FOLDERS_MOVIES))

        movie_folder_name = pretty_path.replace(settings.FOLDERS_MOVIES, '')

        self.failUnlessEqual("Some Random Movie Sequel", movie_folder_name.strip('/'))
        
        path = paths[1]
        path_parts = path.get_handler().file.get_path_parts()

        self.failUnlessEqual(3, len(path_parts), "Was NOT three")
        self.failUnlessEqual(
            ['Some.Random.Movie', 'mapsm.avi', 'Some.Movie.Archive'],
            path_parts,
            path_parts
        )

        pretty_path = path.get_handler().file.get_pretty_path()

        self.failUnless(pretty_path.startswith(settings.FOLDERS_MOVIES))

        movie_folder_name = pretty_path.replace(settings.FOLDERS_MOVIES, '')

        self.failUnlessEqual("Some Random Movie", movie_folder_name.strip('/'))




        #if path.is_interesting():
        #    print "Pretty Path", path.get_handler().file.get_pretty_path()