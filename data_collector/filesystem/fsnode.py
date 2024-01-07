from __future__ import annotations
import os
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

        if not self.get_is_file():
            self.sub_paths : list[str] = [os.path.join(self.path,name) for name in os.listdir(self.path)]
        else:
            self.sub_paths : list[str] = []

    def get_is_file(self):
        return os.path.isfile(self.path)

    def get_xrd_descendants(self) -> list[str]:
        xrd_file_paths = []

        xrd_file_paths += self._get_xrd_subfiles()
        for folder_path in self._get_subdirs():
            xrd_folder = FsNode(path=folder_path)
            xrd_file_paths += xrd_folder.get_xrd_descendants()

        return xrd_file_paths

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

