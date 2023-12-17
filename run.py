from data_collector.configs import set_configs
set_configs()

from kivy.core.window import Window
Window.clearcolor = (1, 1, 1, 1)
import os
from data_collector.datacollectapp import DataCollectApp
# -------------------------------------------


def main():
    # win_test_dir = 'C:\\Users\\daniel\\OneDrive\\Desktop\\test_folder'
    # win_target_test = 'C:\\Users\\daniel\\OneDrive\\Desktop'

    # _, __ = win_test_dir, win_target_test

    linux_input_test = '/home/daniel/aimat/tool_sample_folder'
    # linux_target_test = '/home/work/Desktop'


    app = DataCollectApp(target_folder=os.path.dirname(os.path.abspath(__file__)))
                         # override_input_folder= linux_input_test)

    app.run()

main()