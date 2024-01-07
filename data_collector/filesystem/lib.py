import platform, sys, os

def get_initial_path():
    if platform.system() == 'Windows':
        initial_path = os.path.splitdrive(sys.executable)[0] + '\\'
    else:
        initial_path = '/'

    return initial_path