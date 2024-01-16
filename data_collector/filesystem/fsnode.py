from __future__ import annotations

import copy
import os
from abc import abstractmethod
from typing import Optional
import time

# -------------------------------------------



class FsNode:
    default_xrd_formats : list = ['raw', 'dif', 'gdf', 'dat', 'ras', 'cpi', 'txt', 'plv', 'xrdml']

    time_filesystem_searching = 0
    time_relevancy_sorting = 0

    @classmethod
    def set_default_formats(cls, format_text : str):
        entries = format_text.split(',')
        formats = [entry.strip('.').strip() for entry in entries if '.' in entry]

        cls.default_xrd_formats = formats


    def __init__(self, path : str):
        self.path : str = path
        self.name : str = os.path.basename(path)

        self.potential_xrd_children : list = []
        self.potential_des : list = []
        self.xrd_node_des : list =[]
        self.fsys_dict : Optional[dict] = None


    def initialize_fsys(self):
        start_time = time.time()

        for name in self.get_all_potential_sub():
            child = self.make_child(name=name)
            child.fsys_dict = self.fsys_dict[name]
            self.potential_xrd_children += [child]
        self.time_filesystem_searching += time.time()-start_time


        start_time = time.time()
        self.potential_des = copy.copy(self.potential_xrd_children)
        for child in self.potential_xrd_children:
            child.initialize_fsys()
            self.potential_des += child.potential_des

        for fsys_des in self.potential_des:
            self.xrd_node_des += [fsys_des] if fsys_des.get_is_xrd_relevant() else []
        self.time_relevancy_sorting += time.time()-start_time


    @abstractmethod
    def make_child(self, name : str):
        pass

    # -------------------------------------------
    # get

    def get_all_potential_sub(self):
        fsys_dict = self.get_fsys_dict()
        sub_paths = [os.path.join(self.path, name) for name in list(fsys_dict.keys())]
        potentially_relevant = lambda path : path_is_xrd_file(path) or path_is_dir(path)

        relevant_paths = [path for path in sub_paths if potentially_relevant(path)]
        relevant_names = [os.path.basename(path) for path in relevant_paths]

        return relevant_names


    def get_is_xrd_relevant(self):
        return any([des.get_is_xrd_file() for des in self.potential_des]) or self.get_is_xrd_file()

    def get_is_xrd_file(self):
        is_file = os.path.isfile(self.path)
        is_xrd_format = any([self.path.endswith(f'.{the_format}') for the_format in self.default_xrd_formats])
        return is_file and is_xrd_format

    def get_is_file(self):
        return os.path.isfile(self.path)

    def get_xrd_file_des(self):
        return [node for node in self.xrd_node_des if node.get_is_xrd_file()]

    # -------------------------------------------
    # fsys dict

    def get_fsys_dict(self):
        if self.fsys_dict is None:
            self.fsys_dict = self.make_fsys_dict()

        return self.fsys_dict

    def make_fsys_dict(self) -> dict:
        root_dir = self.path
        file_structure = {}

        for root, dirs, files in os.walk(root_dir, followlinks=True):
            relative_path = root.replace(root_dir, '').lstrip(os.sep)
            current_level = file_structure

            parts = relative_path.split(os.sep)
            for part in parts:
                if part:
                    current_level = current_level.setdefault(part, {})

            for file in files:
                current_level[file] = None

        return file_structure


def path_is_xrd_file(path : str):
    is_file = os.path.isfile(path)
    is_xrd_format = any([path.endswith(f'.{the_format}') for the_format in FsNode.default_xrd_formats])
    return is_file and is_xrd_format

def path_is_dir(path):
    return os.path.isdir(path)
