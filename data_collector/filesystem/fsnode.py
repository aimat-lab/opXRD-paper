from __future__ import annotations
import os, copy
from abc import abstractmethod
# from typing import Optional

# -------------------------------------------


class FsNode:
    default_xrd_formats : list = ['raw', 'dif', 'gdf', 'dat', 'ras', 'cpi', 'txt', 'plv', 'xrdml']

    @classmethod
    def set_default_formats(cls, format_text : str):
        entries = format_text.split(',')
        formats = [entry.strip('.').strip() for entry in entries if '.' in entry]

        cls.default_xrd_formats = formats


    def __init__(self, path : str):
        self.path : str = path
        self.name : str = os.path.basename(path)

        self.active_children : list = []
        self.filestructure_desc : list = []
        self.xrd_node_des : list =[]

        if not self.get_is_file():
            try:
                self.sub_paths : list[str] = [os.path.join(self.path,name) for name in os.listdir(self.path)]
            except:
                self.sub_paths: list[str] = []

        else:
            self.sub_paths : list[str] = []


    @abstractmethod
    def make_child(self, path : str):
        pass

    def recursively_initialize_filestructure(self):
        self.active_children = [self.make_child(path=path) for path in self.get_all_sub()]
        descendants = copy.copy(self.active_children)
        for child in self.active_children:
            child.recursively_initialize_filestructure()
            descendants += child.filestructure_desc

        self.filestructure_desc = descendants

        for fsys_des in self.filestructure_desc:
            self.xrd_node_des += [fsys_des] if fsys_des.get_is_xrd_relevant() else []

    def get_xrd_file_des(self):
        return [node for node in self.xrd_node_des if node.get_is_xrd_file()]

    def get_is_xrd_relevant(self):
        return any([des.get_is_xrd_file() for des in self.filestructure_desc]) or self.get_is_xrd_file()

    def get_is_xrd_file(self):
        return self._get_path_is_xrd_file(path=self.path)


    def get_is_file(self):
        return os.path.isfile(self.path)

    def get_all_sub(self):
        return self._get_xrd_subfiles() + self._get_subdirs()

    # -------------------------------------------

    def _get_subfiles(self) -> list[str]:
        return self._get_subnodes(criterion=lambda x : os.path.isfile(x))

    def _get_subdirs(self) -> list[str]:
        return self._get_subnodes(criterion=lambda x : os.path.isdir(x))

    def _get_xrd_subfiles(self) -> list[str]:
        return self._get_subnodes(criterion=self._get_path_is_xrd_file)

    def _get_path_is_xrd_file(self, path : str):
        is_file = os.path.isfile(path)
        is_xrd_format = any([path.endswith(f'.{the_format}') for the_format in self.default_xrd_formats])
        return is_file and is_xrd_format

    def _get_subnodes(self, criterion : callable):
        return [path for path in self.sub_paths if criterion(path)]

    def get_file_structure(self):
        root_dir = self.path
        file_structure = {}

        for root, dirs, files in os.walk(root_dir):
            relative_path = root.replace(root_dir, '').lstrip(os.sep)
            current_level = file_structure

            parts = relative_path.split(os.sep)
            for part in parts:
                if part:
                    current_level = current_level.setdefault(part, {})

            for file in files:
                current_level[file] = None

        return file_structure