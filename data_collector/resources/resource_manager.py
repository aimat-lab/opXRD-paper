import os
file_path = __file__
dir_path = os.path.dirname(file_path)

def get_foldericon_path() -> str:
    return os.path.join(dir_path,'folder.png')

def get_fileicon_path() -> str:
    return os.path.join(dir_path,'file.png')

def get_collapsed_icon_path() -> str:
    return os.path.join(dir_path,'collapsed.png')

def get_expanded_icon_path() -> str:
    return os.path.join(dir_path,'expanded.png')

def get_loading_icon_path() -> str:
    return os.path.join(dir_path,'loading.png')