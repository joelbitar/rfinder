import os
import re

import settings

from handlers.file import FileHandler
from handlers.rar import RarHandler
from analyzer.analyzer import SortAdapter

import analyzer


ERROR_STR= """Error removing %(path)s, %(error)s """

def rmgeneric(path, __func__):

    try:
        __func__(path)
        #print 'Removed ', path
    except OSError, (errno, strerror):
        print ERROR_STR % {'path' : path, 'error': strerror }

def removeall(path):

    if not os.path.isdir(path):
        return

    files=os.listdir(path)

    for x in files:
        fullpath=os.path.join(path, x)
        if os.path.isfile(fullpath):
            f=os.remove
            rmgeneric(fullpath, f)
        elif os.path.isdir(fullpath):
            removeall(fullpath)
            f=os.rmdir
            rmgeneric(fullpath, f)


class PathPartsSorter(SortAdapter):
    regexps_and_points = (
        ('.*\.?archive\.?.*', -10),
        ('.*\.?pack\.?.*', -20),
        ('.*best.?of\..*', -5),
        ('.*\.\w{3,4}$', -1),
    )

    def get_points(self, string):
        for regexp, points in self.regexps_and_points:
            if re.match(regexp, string.lower()):
                return points

        # Defaults to 0
        return 1


    def __lt__(self, other):
        self_points = self.get_points(self.obj)
        other_points = self.get_points(other.obj)

        # If they did not match is ome odd way like if its a pack or so, we Choose the Longest name.
        if self_points == 0 and other_points == 0:
            return len(self.obj) > len(other.obj)

        # If the Other has less points than me
        return self_points > other_points


class File(object):
    PATH_PART_BLACKLIST = ('',)

    def __init__(self, base_path, path):
        self.base_path = base_path
        self.path = path

    @property
    def full_path(self):
        return os.path.join(
            self.base_path,
            self.path
        )

    def get_path_parts(self):
        path_parts = []
        path_after_base_path = self.path[len(settings.BASE_PATH):]

        for path_part in path_after_base_path.split(os.path.sep):
            if path_part not in self.PATH_PART_BLACKLIST:
                path_parts.append(path_part)

        sorted_path_parts = sorted(path_parts, key=PathPartsSorter)
        return sorted_path_parts

    def get_file_name(self):
        #Gets the last thing in the path, ie movie.avi in /foo/bar/movie.avi
        return self.path.split(os.path.sep)[-1]

    def is_interesting(self):
        # Check for defeite no-nos
        lowercase_parts = [part.lower() for part in self.get_path_parts()]
        if 'sample' in lowercase_parts:
            return False

        return self.get_handler() is not None

    def get_handler(self):
        file_name = self.get_file_name()
        handler = None
        # try out those pesky .partxx.rar files. Abort
        match = re.match(r'.*part_?(\d{1,3})\.rar', file_name)
        if match:
            # we have a match.
            if int(match.group(1)) == 1:
            # Only return a RarHandler if the "part" is 1, (intified, so 001,01 will be ok too
                return RarHandler(self)
            else:
                # If the part was NOT 001, 02 or whatevver, then we want to ABORT.
                return None

        # get the file extension
        match = re.match(r'.*\.(\w{2,4})$', file_name)

        if match and match.group(1) == 'rar':
            return RarHandler(self)

        if match and match.group(1) in settings.MOVIE_FILE_EXTENSIONS:
            return FileHandler(self)

        if match and match.group(1) in settings.MUSIC_FILE_EXTENSIONS:
            return FileHandler(self)

        return None

    def get_analyzer(self):
        return analyzer.analyze(self)

    def get_descriptive_string(self):
        if isinstance(self.get_analyzer(), analyzer.ShowAnalyzer):
            show_properties = self.get_analyzer().get_show_properties()

            episode_number = show_properties.get('episode', None)
            if episode_number is None:
                episode_number = '??'

            season_number = show_properties.get('season', None)
            if season_number is None:
                season_number = '??'

            return "%s - Season %s Episode %s" % (
               repr(show_properties.get('show_name', 'UNKNOWN')),
               repr(season_number),
               repr(episode_number)
            )
        elif isinstance(self.get_analyzer(), analyzer.MovieAnalyzer):
            return " ".join(self.get_pretty_path_list())
        elif isinstance(self.get_analyzer(), analyzer.MusicAnalyzer):
            return " ".join(self.get_pretty_path_list())

    def get_pretty_path(self):
        if settings.VERBOSE > 2:
            print 'File.get_pretty_path()'
            print 'Path from analyzer: %s' % analyzer.analyze(self).get_pretty_path()
        return analyzer.analyze(self).get_pretty_path()

    def get_pretty_path_list(self):
        return analyzer.analyze(self).get_pretty_path_list()


    def __unicode__(self):
        return "%s" % (self.path)
    
    def __str__(self):
        return self.__unicode__()

def find_all_items_in_directory(path):
    return os.listdir(path)

def find_all_files(path, base_path=None):
    if base_path is None:
        base_path = path

    # Check if this is a file
    if os.path.isfile(path):
        yield File(base_path=base_path, path=path)
    else:
        # Loop thru all item in this folder
        for item_in_path in find_all_items_in_directory(path):
            p = os.path.join(path, item_in_path)
            for file_path in find_all_files(p, base_path=base_path):
                yield file_path

    # if is a directory, loop thru files IN this directory
