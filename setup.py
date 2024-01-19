import os.path

from cx_Freeze import setup, Executable
import sys

# GUI applications require a different base on Windows
base = None
if sys.platform == "win32":
    base = "Win32GUI"

home_dirpath = os.path.expanduser("~")
build_dirpath = os.path.join(home_dirpath, 'xrd_data_collect')
build_exe_options = {
    "packages": ["kivy", "os","PIL"],
    "excludes": [],
    "include_files": [],
    "build_exe" : build_dirpath
}

setup(
    name="XRD data collect app",
    version="1.0",
    description="Collects selected XRD data given data folder",
    options={"build_exe": build_exe_options},
    executables=[Executable("data_collector/run/prod_run.py", base=base)]
)