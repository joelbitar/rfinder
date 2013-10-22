__author__ = 'joel'

import os
from rutorrent.rutorrent import ruTorrent
from tracker.tracker import Tracker
from optparse import OptionParser
from files.files import find_all_files
from files.finder import FileFinder
from time import sleep
import shutil
from datetime import datetime

import settings


parser = OptionParser()

parser.add_option('-u', '--url', dest='url', default=None)
parser.add_option('-b', '--basicauth', dest='basic_auth', default=None)
parser.add_option('-p', '--path', dest='path', default=None)
parser.add_option('-v', '--verbose', dest='verbose', default=False)
parser.add_option('-c', '--unpacked_files_count_', dest='unpacked_files_count', default=4)
parser.add_option('-r', '--remove_old_output_compare_file', dest='remove_old_output_compare_file', default="")
parser.add_option('-l', '--logdir', dest='log_dir', default=None)
parser.add_option('-t', '--temp_unpack_path', dest='temp_unpack_path', default=None)
parser.add_option('-o', '--output_path', dest='output_path', default=None)

(options, args) = parser.parse_args()
if options.url is None:
    exit('supply url')

if options.output_path is None:
    print('Output path needs to be specified, -o/--output_path')
    exit()
if options.path is None:
    exit('supply base path')

try:
    settings.VERBOSE = int(options.verbose)
except:
    settings.VERBOSE = 0

settings.FOLDERS_MUSIC = os.path.join(options.output_path, 'music')
settings.FOLDERS_TV_SHOWS = os.path.join(options.output_path, 'shows')
settings.FOLDERS_MOVIES = os.path.join(options.output_path, 'movies')

settings.TEMP_UNPACK_PATH = options.temp_unpack_path

settings.BASE_PATH = options.path


def get_all_directories_in_output():
    empty_directories = [d for d in FileFinder(options.output_path).empty_directories() if d.file_name not in ['movies', 'shows', 'tv']]

    return empty_directories


def remove_empty_directories():
    # Remove empty directories
    empty_directories = get_all_directories_in_output()
    while empty_directories:
        for empty_directory in empty_directories:
            print 'Removing empty directory', empty_directory.path
            try:
                shutil.rmtree(empty_directory.path)
            except OSError:
                print 'Directory not found...'

        empty_directories = get_all_directories_in_output()


def remove_old_output_directories(older_than_path, minutes):
    if not os.path.isfile(older_than_path):
        return False

    older_than_modified_time = datetime.fromtimestamp(os.path.getmtime(older_than_path))

    for e in FileFinder(options.output_path).directories:
        if e.file_name in ['movies', 'shows', 'tv']:
            continue

        if e.modified_time > older_than_modified_time:
            continue

        delta = older_than_modified_time - e.modified_time

        if delta.seconds == 0:
            continue

        not_touched_since_minutes = delta.seconds / 60
        if not_touched_since_minutes < minutes:
            continue

        print 'Removing old directory: ', e
        try:
            shutil.rmtree(e.path)
        except OSError:
            # Already removed
            pass


r = ruTorrent(
    options.url
)
if options.basic_auth:
    r.set_basic_auth_hash(
        options.basic_auth
    )

tracker = Tracker(
    options.log_dir,
    'rutorrent-track'
)

g = r.commands.get_torrent_list()

while True:
    for t in g:
        print '-'*55
        print t.path

        if not t.is_done:
            print 'Not done'
            continue

        if not tracker.is_item_new(t.name, add_item=True):
            print 'Already processed'
            continue

        print 'YAY new'
        print t.id

        for f in find_all_files(t.path):
            if not f.is_interesting():
                continue

            print 'I like!', f

            # We do not want to fill up the disk for nothing now do we?
            while FileFinder(options.output_path).files_count() >= options.unpacked_files_count:
                print 'Files in the output_path, waiting for them to be removed'
                sleep(120)

                # Remove old directories
                remove_old_output_directories(
                    options.remove_old_output_compare_file,
                    300  # Five hours
                )
                # Remove the empty directories
                remove_empty_directories()

            handler = f.get_handler()
            handler.execute()

        print("\n")

    remove_old_output_directories(
        options.remove_old_output_compare_file,
        300  # Five hours
    )
    remove_empty_directories()

    sleep(10)