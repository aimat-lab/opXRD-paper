from data_collector.configs import set_configs
set_configs()

from kivy.core.window import Window
Window.clearcolor = (1, 1, 1, 1)
# import os
from kivy.modules import inspector
from data_collector.datacollectapp import DataCollectApp
# -------------------------------------------


def main():
    # win_test_dir = 'C:\\Users\\daniel\\OneDrive\\Desktop\\test_folder'
    # win_target_test = 'C:\\Users\\daniel\\OneDrive\\Desktop'

    # _, __ = win_test_dir, win_target_test

    # linux_input_test = '/home/daniel/aimat/tool_sample_folder'
    # linux_target_test = '/home/work/Desktop'


    app = DataCollectApp(override_target_folder=f'/home/daniel/aimat/tool_target_folder',
                         override_input_folder=f'/home/daniel/aimat/tool_sample_folder')
    inspector.create_inspector(Window, app)

    app.run()

main()