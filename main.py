#! /usr/bin/python

import os
import sys
from optparse import OptionParser
import datetime
from supertweet import supertweet
import yaml

import simplejson

import settings
from files import files
from models import directory

parser = OptionParser()
parser.add_option('-p', '--path', dest='path', default=None)
parser.add_option('-v', '--verbose', dest='verbose', default=False)
parser.add_option('-d', '--dryrun', dest='dry_run', default=False)
parser.add_option('-j', '--json', dest='get_json_args', default=False)
parser.add_option('-c', '--current_path', dest='use_current_path_as_base', default=True)
parser.add_option('-r', '--remove', dest='remove_after_action', default=True)

(options, args) = parser.parse_args()

if options.path is not None:
   args.append(options.path)

try:
   settings.VERBOSE = int(options.verbose)
except:
   settings.VERBOSE = 0

settings.DRY_RUN = options.dry_run != False
settings.DELETE_SOURCE_AFTER_ACTION = options.remove_after_action != False
settings.DELETE_SOURCE_AFTER_ACTION = False

execute_paths = []

for arg in args:
   if options.use_current_path_as_base:
      execute_paths.append(os.path.join(os.getcwd(), arg))

if options.get_json_args is not False:
   print 'Settings'
   print 'verbose', settings.VERBOSE
   print 'dry run', settings.DRY_RUN
   print 'delete after', settings.DELETE_SOURCE_AFTER_ACTION
   print 'exec paths'
   print execute_paths
   print options
   print args
   exit()

config_file_path = '/home/%s/.rfinder/config.yml' % ('joel')
# Is there a config file

print 'Running'

def get_all_files(path, extensions):
    for file in os.listdir(path):
        full_path = os.path.join(path, file)
        if os.path.isfile(full_path) and True in [file.endswith('.%s' % ext) for ext in extensions]:
            yield full_path

if os.path.exists(config_file_path):
    config_file_content = open(config_file_path).read()
    config = yaml.load(config_file_content)
else:
    config = {'twitter':
        {
            'username': '',
            'password': '',
            'url': ''
        }
    }

    config_file_content = yaml.dump(config)
    config_file = open(config_file_path, 'w')
    config_file.write(config_file_content)


settings.config = config



if not execute_paths:
    print 'downloads folder:', settings.DOWNLOADS_FOLDER
    for path in os.listdir(settings.DOWNLOADS_FOLDER):
        full_path = os.path.join(settings.DOWNLOADS_FOLDER, path)
        print 'Full path: ', full_path
        execute_paths.append(full_path)

print execute_paths

# Run on the paths submitted to us.
for execute_path in execute_paths:
    print 'Path: ', execute_path

    results = []

    if settings.VERBOSE:
        pass

    print 'Start the analyzing'
    take_action = False
    d = directory.get_dir(dir_name = execute_path)
    
    print 'Directory', d
    
    # The directory is 
    if d is None:
        if settings.VERBOSE:
            print 'Creating the directory in the database'

        take_action = True
        
        d = directory.create_directory(
           dir_name = execute_path,
           path_name = settings.DOWNLOADS_FOLDER,
           checked = datetime.datetime.now()
        )
    else:
        # The directory is old, now we are gonna check if it's old.
        if settings.VERBOSE:
            print 'The directory is in the database. NOT going to take action'
        # If we should not delete the source after action
        # OR
        # the directory is not OLD
        if not settings.DELETE_SOURCE_AFTER_ACTION:
            if settings.VERBOSE:
                print 'We should not delete the soruce after action'
            continue
        
        if not d.is_old():
            if settings.VERBOSE:
                print 'The directory is NOT old, aborting.'
            continue

    # we should take action
    if take_action:
        for path in files.find_all_files(execute_path):
            handler = None
            if path.is_interesting():
                print "Is interesting", path
                handler = path.get_handler()
                print handler
                success = handler.execute()
                results.append(success)
    else:
        if settings.VERBOSE:
            print 'Did NOT take action'

    if False not in results and settings.DELETE_SOURCE_AFTER_ACTION or d.is_old():
        print 'REMOVING', execute_path
        files.removeall(execute_path)
        if os.path.isfile(execute_path):
            os.remove(execute_path)
        else:
            os.rmdir(execute_path)

        # After we delete the "physical" directory, delete the representation in the Database
        directory.Directory.delete(d.id)

