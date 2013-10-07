import os
import sys
import datetime

from sqlobject import *

project_path = os.path.split(sys.path[0])[0]

if os.path.split(project_path)[1] == 'rfinder':
   sys.path.append(project_path)

import settings

db_filename = os.path.abspath(settings.DATABASE_PATH)


if False:
   if os.path.exists(db_filename):
      os.unlink(db_filename)

connection_string = 'sqlite:' + db_filename
connection = connectionForURI(connection_string)
sqlhub.processConnection = connection

class Directory(SQLObject):
   dir_name = StringCol()
   path_name = StringCol()
   checked = DateTimeCol()

   def is_old(self):
       time_delta = datetime.timedelta(days=settings.DELETE_SOURCE_AFTER_DAYS)
       return datetime.datetime.now() > self.checked + time_delta
       


def get_dir(**kwargs):
    dir = Directory.select(
        Directory.q.dir_name == kwargs.get('dir_name')
    )

    if len(list(dir)) == 0:
        return None
    elif len(list(dir)) == 1:
        return dir[0]
    else:
        return dir



def create_directory(**kwargs):
    dir = get_dir(**kwargs)

    if dir is None:
        return Directory(**kwargs)
    else:
        return dir

if not os.path.exists(db_filename):
   print 'database does not exist, creating it.'
   Directory.createTable()
