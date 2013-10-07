import re

import settings
from analyzer import Analyzer

class MovieAnalyzer(Analyzer):

    def get_movie_name(self):
        regexps = []
        for stop_word in ['(\d{4})', '720p', 'DVDRip', 'BlueRay', 'XviD', 'DivX', 'Remastered', 'h264']:
            regexps += [r'(.*)[\s\-_\.]{0,2}%s.*' % stop_word]

        for path_part in self.file.get_path_parts():
            print 'Path part;', path_part
            if settings.VERBOSE > 2:
                print 'MovieAnalyzer.get_move_name()'
                print 'Path part: %s' % (path_part)
                print ''

            for regexp in regexps:
                match = re.match(regexp, path_part, re.IGNORECASE)
                if match:
                    if settings.VERBOSE > 3:
                        print 'MovieAnalyzer.get_move_name()'
                        print 'Match on regexp: %s, path: %s' % (regexp, path_part)
                        print 'Matches: %s' % (repr(match.groups()))
                        print ''

                    cleaned_name = self.get_cleaned_name(" ".join(match.groups()))
                    if cleaned_name:
                        return cleaned_name

        if settings.VERBOSE > 2:
            print 'MovieAnalyzer.get_move_name()'
            print 'Could not find a good name to match against'
            print ''

        for path_part in self.file.get_path_parts():
            cleaned_name = self.get_cleaned_name(path_part)
            if cleaned_name:
                return cleaned_name

    def get_pretty_path_list(self):
        return [self.get_movie_name()]

    def get_pretty_path(self):
        pretty_path = self.get_absolut_path(
           [settings.FOLDERS_MOVIES] + self.get_pretty_path_list()
        )

        if settings.VERBOSE > 1:
            print 'MovieAnalyzer.get_pretty_path()'
            print 'Pretty path: %s' % (pretty_path)
            print [settings.FOLDERS_MOVIES] + self.get_pretty_path_list()

        return pretty_path

    def get_confidence(self):
        return 10
