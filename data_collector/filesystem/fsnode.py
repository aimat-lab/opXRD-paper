from __future__ import annotations
import os, copy
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
        self.potential_des : list = []
        self.relevant_des : list =[]
        self.xrd_file_des : list = []

        if not self.get_is_file():
            self.sub_paths : list[str] = [os.path.join(self.path,name) for name in os.listdir(self.path)]
        else:
            self.sub_paths : list[str] = []


    def recursively_initialize_filestructure(self):
        descendants = copy.copy(self.active_children)
        for child in self.active_children:
            child.recursively_initialize_filestructure()
            descendants += child.potential_des

        self.potential_des = descendants
        relevant_des = []
        for outer_des in self.potential_des:
            is_relevant = any([des.get_is_file() for des in outer_des.potential_des]) or outer_des.get_is_file()
            relevant_des += [outer_des] if is_relevant else []

        self.relevant_des = relevant_des
        self.xrd_file_des = [des for des in self.relevant_des if des.get_is_file()]


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

