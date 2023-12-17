from kivy.config import Config
from screeninfo import get_monitors

# -------------------------------------------

def get_primary_monitor():
    monitors = get_monitors()
    for monitor in monitors:
        if monitor.is_primary:
            return monitor
    return None

def set_configs():
    Config.set('graphics', 'fullscreen', 0)
    Config.set('graphics', 'resizable', '0')

    primary_monitor = get_primary_monitor()

    relative_width = 0.5
    relative_height = 0.75

    Config.set('graphics', 'width', str(int(primary_monitor.width*relative_width)))
    Config.set('graphics', 'height', str(int(primary_monitor.height*relative_height)))
    Config.set('graphics', 'left', str(primary_monitor.x))
    Config.set('graphics', 'top', str(primary_monitor.y))
    Config.write()


