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

class ExtractMovieNames(TestCase):
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


    def testRunOnEntireTestFolder(self):
        for execute_path in os.listdir(self.base_path):
            print '#' * 50
            print "# Working with dir: ", execute_path
            paths = files.find_all_files(os.path.join(self.base_path, execute_path))
            for pa in paths:
                print "#", pa.is_interesting(), '|', pa
                if pa.is_interesting():
                    pa.get_handler().execute()

                d = directory.get_dir(dir_name = execute_path)
                # If the directory is not in the database
                if not d:
                    d = directory.create_directory(
                       dir_name = execute_path,
                       path_name = self.base_path,
                       checked = datetime.now()
                    )
                    # Brand spanking new
                else:
                    if d.is_old():
                        print 'Dir is old'
                        continue

                print "#", pa.get_descriptive_string()

    def testExtractWeirdShowName(self):
        for path in files.find_all_files(os.path.join(self.base_path, 'Nile City 105.6')):
            if path.is_interesting():
                path.get_handler().execute()

    def testUnrarMovie(self):
        for path in files.find_all_files(os.path.join(self.base_path, 'Big.Buck.Bunny')):
            if path.is_interesting():
                path.get_handler().execute()


    def test_should_work_with_movie_packs(self):
        for path in files.find_all_files(os.path.join(self.base_path, 'Some.Movie.Archive')):
            print path
            path_parts = path.get_handler().file.get_path_parts()



            if path.is_interesting():
                print "Pretty Path", path.get_handler().file.get_pretty_path()