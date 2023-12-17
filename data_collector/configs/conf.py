import sys
import ctypes
from kivy.config import Config
from screeninfo import get_monitors
import logging

logging.basicConfig(level=logging.INFO)
# -------------------------------------------

def get_primary_monitor():
    monitors = get_monitors()
    for monitor in monitors:
        if monitor.is_primary:
            return monitor
    return None

def get_scaling_factor():
    ui_scale = 1
    if sys.platform == 'win32':
        try:
            ui_scale = ctypes.windll.shcore.GetScaleFactorForDevice(0) / 100
        except:
            pass


    return ui_scale

def set_configs():
    Config.set('graphics', 'fullscreen', 0)
    Config.set('graphics', 'resizable', '0')

    primary_monitor = get_primary_monitor()
    scaling_factor = get_scaling_factor()

    relative_width = 0.5
    relative_height = 0.75

    app_width = int(primary_monitor.width * relative_width / scaling_factor)
    app_height = int(primary_monitor.height * relative_height / scaling_factor)

    print(f'[INFO]: Unscaled width, height: {app_width},{app_height}')

    Config.set('graphics', 'width', str(app_width))
    Config.set('graphics', 'height', str(app_height))
    # Config.set('graphics', 'left', str(primary_monitor.x * scaling_factor))
    # Config.set('graphics', 'top', str(primary_monitor.y * scaling_factor))
    Config.write()

# Call set_configs() at the appropriate place in your application initialization
