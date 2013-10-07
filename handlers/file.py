import shutil
import os

from handler import Handler

import settings

class FileHandler(Handler):
    def execute(self):
        if settings.VERBOSE:
            print 'FileHandler'
            print "Copy: %s" % (self.file.full_path)
            print "To: %s" % (self.file.get_pretty_path())

        if settings.DRY_RUN:
            print '!!! Dry run, Aborted'
            return False

        super(FileHandler, self).execute()

        temp_directory = self.get_temp_folder_path()
        temp_file_path = os.path.join(
            temp_directory,
            'file'
        )

        self.create_target_path(
            temp_directory
        )

        print 'Copying file to temp dir...'
        shutil.copyfile(
            self.file.full_path,
            temp_file_path
        )

        print 'Moving file to final path...'
        shutil.move(
            temp_file_path,
            os.path.join(self.file.get_pretty_path(), self.file.get_file_name())
        )

        print "Done!"

        super(FileHandler, self).post_execute()

        return True

