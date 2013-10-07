import re

import settings

class SortAdapter(object):
    def __init__(self, obj):
        self.obj = obj

class MatchesSorter(SortAdapter):
    def __lt__(self, other):
        return self.obj[0] > other.obj[0]


class Analyzer(object):
    def __init__(self, file):
        self.file = file

    def get_matches(self):
        matches = []
        for path_part in self.file.get_path_parts():
            for pattern, confidence, mapping in self.patterns_and_values:
                match = re.match(pattern, path_part, re.IGNORECASE)

                if not match:
                    continue

                matches.append(
                   (
                      confidence,
                      match.groups(),
                      mapping
                   )
                )

        if not matches:
            return matches

        return sorted(matches, key=MatchesSorter)

    def get_cleaned_name(self, name):
        cleaned_name = name
        
        cleaned_name = re.sub(r"\[.*]*\]+", '', cleaned_name)
        cleaned_name = re.sub(r"\{.*]*\}+", '', cleaned_name)
        cleaned_name = re.sub('[\W_]', ' ', cleaned_name)
        cleaned_name = re.sub('(\s)\\1+','\\1', cleaned_name)

        if settings.CAPITALIZE_FOLDER_NAMES:
            cleaned_name = " ".join([part.capitalize() for part in cleaned_name.split(' ')])

        return cleaned_name.strip(' ')


    def get_confidence(self):
        raise NotImplementedError('confidence HAS to be implented on analyzers')

    def get_pretty_path(self):
        return 'FOLDER'

    def get_absolut_path(self, path_list):
        return '/'.join(path_list).rstrip('/') + '/'

    def __getattr__(self, name):
        return {
           'confidence' : self.get_confidence()
        }.get(name, None)
