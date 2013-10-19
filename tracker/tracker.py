__author__ = 'joel'
import os


class Tracker(object):
    def __init__(self, track_path, track_file_name):
        self.__track_path = track_path
        self.__track_file_name = track_file_name

    @property
    def track_path(self):
        return self.__track_path

    def get_track_file_path(self):
        path = os.path.join(
            self.track_path, self.__track_file_name
        )

        return path

    def clear(self):
        self.write_track_file(
            self.get_track_file_path(),
            []
        )

    def write_track_file(self, path, items):
        f = open(path, 'w')
        f.close()

        for item in items:
            self.add_item_to_tracker_file(item)

    def get_items_in_tracker_file(self):
        path = self.get_track_file_path()

        if not os.path.exists(path):
            self.write_track_file(
                path,
                None
            )
            return []

        f = open(path, 'r')

        lines = f.readlines()
        f.close()

        return [l.strip() for l in lines]

    def add_item_to_tracker_file(self, item):
        if item in self.get_items_in_tracker_file():
            return False

        track_file_path = self.get_track_file_path()

        f = open(track_file_path, 'a')
        f.write(item)
        f.write('\n')
        f.close()

        return True

    def is_item_new(self, item, add_item):
        if item in self.get_items_in_tracker_file():
            return False

        if add_item:
            self.add_item_to_tracker_file(item)

        return True
