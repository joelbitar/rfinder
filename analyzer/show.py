import re

import settings
from analyzer import Analyzer


class ShowAnalyzer(Analyzer):
    patterns_and_values = [
        (r'.*season[\s_\-\.](\d{1,2}).*', 60, ('season', None)),
        (r'.*season(\d{1,2}).*', 60, ('season', None)),
        (r'.*s(\d{1,2})[ex](\d{1,2}).*', 80, ('season', 'episode')),    # ____s01e01____
        (r'.*s(\d{1,2}).*', 40, ('season', None)),
        (r'^(\d)(\d{2})\s\-\s.*', 30, ('season', 'episode')),           # 101 ______
        (r'.*\.(\d)[ex](\d{2})\..*', 30, ('season', 'episode')),      # ____1x01 ______
        (r'.*(\d{4})\.e(\d{1,2}).*', 20, ('season', 'episode')),        # ____213.E10___
        (r'.*\.(\d{4})\.\d{2}\.\d{2}\..*', 18, ('season', None)),
        (r'.*[\.\s]ep(\d{1,2}).*', 15, ('episode', None)),
        (r'.*[\.\s]episode(\d{1,2}).*', 15, ('episode', None)),
        (r'^.*[\s\.\-]e(\d{1,2})[\s\.\-].*', 20, ('episode', None)), # ___E01___
        ]
    def get_confidence(self):
        # Now.. for the fun part!
        confidences = [0]

        for confidence, match, mapping in self.get_matches():
            confidences.append(confidence)

        return max(confidences)
        # Match the folder names

    def get_season(self):
        confidence, match_groups, mapping = self.get_matches()[0]

        if 'season' in mapping:
            try:
                return int(match_groups[mapping.index('season')])
            except:
                pass

        return None


    def get_episode(self):
        confidence, match_groups, mapping = self.get_matches()[0]

        if 'episode' in mapping:
            try:
                return int(match_groups[mapping.index('episode')])
            except:
                pass

        return None

    def get_show_properties(self):
        season = self.get_season()
        episode = self.get_episode()

        return {
            'season' : season,
            'episode' : episode,
            'show_name' : self.get_show_name()
        }

    def get_show_name(self):
        showname_regexps = (
            r'(.*)[\s_\-\.]+complete[\s_\-\.]+season.*',
            r'(.*)[\s_\-\.]+season.*',
            r'(.*)\.\d{4}\.\d{2}\.\d{2}\..*', #Talkshow kind of thing
            r'(.*)\.\d{4}\.e\d{2}\..*', # Other shows, based on year.
            r'(.*)\.\d[ex]\d{2}\..*',
            r'(.*)[\s_\-\.]+s\d{1,2}.*', # Show.s01
            r'(.*)[\s_\-\.]+s\d{1,2}[ex]\d{1,2}[\s_\-\.].*',
            r'(.*)[\s_\-\.]\d{3}.*',
            r'(.*)[\s_\-\.]e\d{2}.*',
        )
        # Iterate of over the paths backwards
        for path_part in self.file.get_path_parts():
            for regexp in showname_regexps:
                match = re.match(regexp,path_part, re.IGNORECASE)
                cleaned_name = False
                if match:
                    cleaned_name = self.get_cleaned_name(" ".join(match.groups()))

                if cleaned_name:
                    return cleaned_name

        for path_part in self.file.get_path_parts():
            cleaned_name = self.get_cleaned_name(path_part)
            if cleaned_name:
                return cleaned_name

    def get_pretty_path_season_name(self):
        season = self.get_season() or 1
        season_str = str(season)

        if len(season_str) == 4:
            return str(season)

        if season <= 9:
            season_str = '0' + season_str

        return "%s %s" % (
            settings.SEASON_FOLDER_NAME,
            season_str
        )


    def get_pretty_path_list(self):
        return [
            self.get_show_name(),
            self.get_pretty_path_season_name()
        ]

    def get_pretty_path(self):
        pretty_path = self.get_absolut_path(
            [settings.FOLDERS_TV_SHOWS] + self.get_pretty_path_list()
        )
        if settings.VERBOSE:
            'Pretty path: %s' % (pretty_path)

        return pretty_path

