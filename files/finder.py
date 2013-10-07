__author__ = 'joel'

import os
from datetime import datetime


class FileSystemEntity(object):
    __base_path = None
    __path_parts = []
    __children = []

    def __init__(self, base_path, path_parts):
        self.__base_path = base_path
        self.__path_parts = path_parts
        self.__children = []

    def add_child(self, child):
        self.__children.append(child)

    @property
    def children(self):
        return self.__children

    @property
    def base_path(self):
        return self.__base_path

    @property
    def path_parts(self):
        return self.__path_parts

    @property
    def path(self):
        return os.path.join(
            self.base_path,
            *self.path_parts
        )

    @property
    def modified_time(self):
        d = datetime.fromtimestamp(
            os.path.getmtime(
                self.path
            )
        )
        return d

    @property
    def is_file(self):
        return os.path.isfile(self.path)

    @property
    def is_directory(self):
        return not self.is_file()

    @property
    def is_empty(self):
        return len(self.children) == 0

    @property
    def file_name(self):
        return self.path_parts[-1]

    def __str__(self):
        return self.path

    def __unicode__(self):
        return self.path


class FileSystemEntities(object):
    __entities = None

    def __init__(self, entities):
        self.__entities = entities

    def __iter__(self):
        for entity in self.__entities:
            yield entity

    def __len__(self):
        return len(self.__entities)


class FileFinder(object):
    __base_path = None
    __entities = None

    def __init__(self, base_path):
        self.__base_path = base_path
        self.__entities = []

    @property
    def base_path(self):
        return self.__base_path

    @property
    def entities(self):
        return self.get_entities()

    @property
    def files(self):
        for e in self.entities:
            if not e.is_file:
                continue

            yield e

    @property
    def directories(self):
        for e in self.entities:
            if e.is_file:
                continue

            yield e

    def count(self):
        return len(self.entities)

    def files_count(self):
        return len([f for f in self.files])

    def get_entities(self):
        if self.__entities:
            return self.__entities

        entities = FileSystemEntities(
            [e for e in self.find_all_files(FileSystemEntity(self.base_path, []))]
        )

        self.__entities = entities

        return entities

    def find_all_files(self, parent_entity):
        if os.path.isfile(parent_entity.path):
            yield parent_entity
            return

        # Loop thru all item in this folder
        for item_in_path in os.listdir(parent_entity.path):
            item_in_path_path_parts = parent_entity.path_parts + [item_in_path]
            i = FileSystemEntity(base_path=self.base_path, path_parts=item_in_path_path_parts)
            for child_item in self.find_all_files(i):
                parent_entity.add_child(child_item)
                yield child_item

        # If this parent is NOT the same as the base path, then I'm good.
        if parent_entity.path is not self.base_path:
            yield parent_entity

    def all_with_extension(self, extension):
        for entity in self.files:
            if not entity.file_name.endswith("." + extension):
                continue

            yield entity

        return

    def all_without_extension(self, extension):
        for entity in self.files:
            if entity.file_name.endswith("." + extension):
                continue

            yield entity

        return

    def all(self):
        return self.entities

    def empty_directories(self):
        for e in self.directories:
            if not e.is_empty:
                continue

            yield e

    def __nonzero__(self):
        return self.count() > 0