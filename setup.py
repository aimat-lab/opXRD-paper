from cx_Freeze import setup, Executable
import sys

# GUI applications require a different base on Windows
base = None
if sys.platform == "win32":
    base = "Win32GUI"

build_exe_options = {
    "packages": ["kivy", "os","PIL"],
    "excludes": [],
    "include_files": []
}

setup(
    name="SimpleKivyApp",
    version="0.1",
    description="My Kivy GUI application!",
    options={"build_exe": build_exe_options},
    executables=[Executable("run.py", base=base)]
)