from data_collector.configs import set_configs
set_configs()

from kivy.core.window import Window
Window.clearcolor = (1, 1, 1, 1)

from kivy.modules import inspector
from data_collector.app import DataCollectApp
# -------------------------------------------


def main():
    win_test_dir = 'C:\\Users\\daniel\\OneDrive\\Desktop\\test_folder'
    win_target_test = 'C:\\Users\\daniel\\OneDrive\\Desktop'

    _, __ = win_test_dir, win_target_test

    linux_input_test = '/home/daniel/aimat'
    linux_target_test = f'/home/daniel/aimat/tool_target_folder'

    app = DataCollectApp(override_input_folder=linux_input_test,
                         override_target_folder=linux_target_test)
    inspector.create_inspector(Window, app)

    app.run()

main()