from pyunrar import RarFile

from handler import Handler

import os
import settings
from datetime import datetime
import shutil

from files.finder import FileFinder

class RarHandler(Handler):
    def unpack(self, rar_file_path, target_path):
        try:
            rar_file = RarFile(rar_file_path)
            rar_file.extract(path=target_path)
            return True
        except:
            pass

        return False

    def execute(self):
        temp_folder_path = None

        if settings.TEMP_UNPACK_PATH is not None:
            temp_folder_path = self.get_temp_folder_path()

        if settings.VERBOSE:
            print 'RarHandler'
            print 'Execute unrar command for %s' % self.file.full_path
            if settings.TEMP_UNPACK_PATH is not None:
                print 'TEMP folder:', temp_folder_path
            print 'Target folder: %s' % self.file.get_pretty_path()

        if settings.DRY_RUN:
            print '!!! Dry run, Aborted'
            return False

        # Create the target path (we might not use it for a while)
        self.create_target_path(temp_folder_path)
        success = self.unpack(
            rar_file_path=self.file.full_path,
            target_path=temp_folder_path
        )

        if success and temp_folder_path is not None:
            for f in FileFinder(temp_folder_path).all_with_extension('rar'):
                self.unpack(
                    f.path,
                    temp_folder_path
                )

        # If we extracted in a temp dir. move the whole shebang to the real folder (Except rar files)
        if success:
            self.create_target_path(self.file.get_pretty_path())
            for entity in FileFinder(temp_folder_path).all_without_extension('rar'):
                shutil.move(
                    entity.path,
                    os.path.join(self.file.get_pretty_path(), entity.file_name)
                )

            # Remove the tempdir
            shutil.rmtree(temp_folder_path)
        else:
            print 'TODO: Should remove the temp folder path...'

        super(RarHandler, self).post_execute()

        return success
