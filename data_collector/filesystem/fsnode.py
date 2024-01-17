from __future__ import annotations

import copy
import os
from abc import abstractmethod
from typing import Optional
import time

from data_collector.filesystem.lib import make_fsys_dict

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
        self.potential_xrd_des : list = []
        self.xrd_node_des : list =[]

        self.fsys_dict : Optional[dict] = None
        self.cached_is_xrd_relevant : Optional[bool] = None


    def init_fsys(self):
        fsys_start = time.time()
        self.initialize_potential_des()
        FsNode.time_filesystem_searching += time.time()-fsys_start

        sorting_start = time.time()
        self.find_xrd_relevant_nodes()
        FsNode.time_relevancy_sorting += time.time()-sorting_start


    def initialize_potential_des(self):
        for name in self.get_all_potential_sub():
            child = self.make_child(name=name)
            child.fsys_dict = self.fsys_dict[name]
            self.potential_xrd_children += [child]

        self.potential_xrd_des = copy.copy(self.potential_xrd_children)
        for child in self.potential_xrd_children:
            child.init_fsys()
            self.potential_xrd_des += child.potential_xrd_des


    def find_xrd_relevant_nodes(self):
        for fsys_des in self.potential_xrd_des:
            self.xrd_node_des += [fsys_des] if fsys_des.get_is_xrd_relevant() else []

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
        if not self.cached_is_xrd_relevant is None:
            return self.cached_is_xrd_relevant

        if self.get_is_file():
            self.cached_is_xrd_relevant = self.get_is_xrd_file()

        else:
            self.cached_is_xrd_relevant = any([child.get_is_xrd_relevant() for child in self.potential_xrd_children])

        return self.cached_is_xrd_relevant

    def get_is_xrd_file(self):
        return path_is_xrd_file(path=self.path)

    def get_is_file(self):
        return os.path.isfile(self.path)

    def get_xrd_file_des(self):
        return [node for node in self.xrd_node_des if node.get_is_xrd_file()]

    def get_fsys_dict(self):
        if self.fsys_dict is None:
            self.fsys_dict = make_fsys_dict(root_dir=self.path)

        return self.fsys_dict


def path_is_xrd_file(path : str):
    is_file = os.path.isfile(path)
    is_xrd_format = any([path.endswith(f'.{the_format}') for the_format in FsNode.default_xrd_formats])
    return is_file and is_xrd_format

def path_is_dir(path):
    return os.path.isdir(path)

