import os
file_path = __file__
images_folder_path = os.path.join(os.path.dirname(file_path), 'images')

def get_blended_logo_path() -> str:
    return os.path.join(images_folder_path,'blended_logo.png')

def get_logo_path() -> str:
    return os.path.join(images_folder_path, 'logo.png')

def get_foldericon_path() -> str:
    return os.path.join(images_folder_path, 'folder.png')

def get_fileicon_path() -> str:
    return os.path.join(images_folder_path, 'file.png')

def get_collapsed_icon_path() -> str:
    return os.path.join(images_folder_path, 'collapsed.png')

def get_expanded_icon_path() -> str:
    return os.path.join(images_folder_path, 'expanded.png')

def get_loading_icon_path() -> str:
    return os.path.join(images_folder_path, 'loading.png')

def get_checked_box_path() -> str:
    return os.path.join(images_folder_path, 'checked_box.png')

def get_unchecked_box_path() -> str:
    return os.path.join(images_folder_path, 'unchecked_box.png')


# -----

doc_folder_path = os.path.join(os.path.dirname(file_path), 'documents')

def get_template_csv() -> str:
    return os.path.join(doc_folder_path, 'template.csv')