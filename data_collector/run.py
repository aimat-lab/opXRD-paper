from kivy.config import Config
Config.set('graphics', 'fullscreen', 0)  # Can use 'auto' or '1'
Config.set('graphics', 'resizable', '0')

import os
from kivy.core.window import Window
from data_collector.datacollectapp import DataCollectApp

# -------------------------------------------

def main():
    # win_test_dir = 'C:\\Users\\daniel\\OneDrive\\Desktop\\test_folder'
    # win_target_test = 'C:\\Users\\daniel\\OneDrive\\Desktop'

    # _, __ = win_test_dir, win_target_test

    linux_input_test = '/home/work/Desktop'
    # linux_target_test = '/home/work/Desktop'

    Window.clearcolor = (1, 1, 1, 1)  # RGBA for white
    app = DataCollectApp(target_folder=os.path.dirname(os.path.abspath(__file__)),
                         override_input_folder= linux_input_test)


    app.run()

if __name__ == "__main__":
    main()