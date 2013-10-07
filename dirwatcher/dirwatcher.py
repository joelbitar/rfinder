__author__ = 'joel'
import os
from time import sleep


class Item(object):
    __name = None
    __base_directory = None

    def __init__(self, name, base_directory):
        self.__name = name
        self.__base_directory = base_directory

    @property
    def name(self):
        return self.__name

    @property
    def base_directory(self):
        return self.__base_directory

    @property
    def full_path(self):
        return os.path.join(
            self.base_directory,
            self.name
        )

    def __unicode__(self):
        return self.full_path

    def __str__(self):
        return self.__unicode__()


class DirWatcher(object):
    __path = None
    __log_path = None
    __sleep_time = 1

    def __init__(self, path):
        self.__path = path

    def set_log_path(self, log_path):
        self.__log_path = log_path

    @property
    def path(self):
        return self.__path

    @property
    def log_path(self):
        return self.__log_path

    def get_log_file_path(self):
        path = os.path.join(
            self.log_path, 'current_files'
        )

        return path

    def write_log_file(self, path, items):
        f = open(path, 'w')
        f.close()

        for item in items:
            self.add_item_to_log(item)

    def get_paths_in_log(self):
        path = self.get_log_file_path()

        if not os.path.exists(path):
            self.write_log_file(
                path,
                None
            )
            return []

        f = open(path, 'r')

        lines = f.readlines()
        f.close()

        return [l.strip() for l in lines]

    def add_item_to_log(self, item):
        if item.full_path in self.get_paths_in_log():
            return False

        log_file_path = self.get_log_file_path()

        f = open(log_file_path, 'a')
        f.write(item.full_path)
        f.write('\n')
        f.close()

        return True

    def is_item_new(self, item):
        if item.full_path in self.get_paths_in_log():
            return False

        return True

    def get_items_in_watch_directory(self):
        items_in_directory = os.listdir(self.path)

        items = []
        for item_in_directory in items_in_directory:
            items.append(
                Item(item_in_directory, self.path)
            )

        return items

    def get_new_items_in_directory(self):
        items_in_watch_dir = self.get_items_in_watch_directory()
        for item in items_in_watch_dir:
            if self.is_item_new(item):
                self.add_item_to_log(item)
                yield item

        self.write_log_file(
            self.get_log_file_path(),
            items_in_watch_dir
        )
        return

    def __iter__(self):
        while True:
            for item in self.get_new_items_in_directory():
                yield item

            sleep(self.__sleep_time)
        return

