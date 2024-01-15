import os
from datetime import datetime
from typing import Optional
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.textinput import TextInput

from data_collector.filesystem import zip_file_list, produce_csv_file
from data_collector.elements import NodeWidget, InputDialog, BlackLabel
from data_collector.elements import get_ok_button, get_feedback_widget
from data_collector.elements import SelectionLayout


# -------------------------------------------

class DataCollectApp(App):
    def __init__(self, override_input_folder : Optional[str]  = None,
                       override_target_folder : Optional[str] = None):
        self.icon = None    
        super(DataCollectApp, self).__init__()

        # Properties
        self.title : str = 'AiMAT XRD data collect'
        self.input_folder_override : Optional[str]  = override_input_folder
        self.targt_folder_override : Optional[str] = override_target_folder
        self.default_font_size = Window.width*0.018

        # PathCheckbox
        self.root_checkbox : Optional[NodeWidget] = None
        self.feedback_widget : Optional[Widget] = None
        self.selection_layout : Optional[SelectionLayout] = None

        self.target_path_input : Optional[Widget] = None


    def build(self):
        self.selection_layout = SelectionLayout(rootCheckbox=self.root_checkbox)
        finish_layout = self.make_finish_layout()

        root_layout = BoxLayout(orientation='vertical')
        root_layout.add_widget(self.selection_layout)
        root_layout.add_widget(finish_layout)

        return root_layout


    def make_finish_layout(self):
        finish_layout = BoxLayout(orientation='vertical',size_hint =(1,0.125))
        upper_finish = BoxLayout(orientation='horizontal', size_hint=(1, 0.4))

        note = BlackLabel(text='Target folder:',size_hint=(0.2,1), font_size = Window.width * 0.02, bold=True)

        self.target_path_input = TextInput(text=f'{os.getcwd()}',
                                    size_hint=(0.7, 1),
                                    font_size=Window.width * 0.02,
                                    multiline=False)
        buffer = BlackLabel(text='',size_hint=(0.1,1))

        upper_finish.add_widget(note)
        upper_finish.add_widget(self.target_path_input)
        upper_finish.add_widget(buffer)

        lower_finish = BoxLayout(orientation='horizontal',size_hint =(1,0.6))
        ok_button = get_ok_button()
        ok_button.bind(on_press=self.produce_dataset_files)

        lower_finish.add_widget(ok_button)
        self.feedback_widget = get_feedback_widget(font_size=self.default_font_size)
        lower_finish.add_widget(self.feedback_widget)

        finish_layout.add_widget(upper_finish)
        finish_layout.add_widget(lower_finish)

        return finish_layout


    def on_start(self):
        if self.input_folder_override is None:
            self.show_launch_dialog(callback=self.selection_layout.set_content)
        else:
            self.selection_layout.set_content(path=self.input_folder_override)

    @staticmethod
    def show_launch_dialog( callback : callable):
        InputDialog(callback=callback).open()

    # -------------------------------------------
    # callbacks



    def produce_dataset_files(self, *args):
        _ = args
        print('Triggered callback of ok button')
        checked_paths = self.get_checked_filepaths()

        current_date = datetime.now()
        datetime_stamp = current_date.strftime('%d_%m_%Y_%H_%M_%S')

        target_folder_path = self.get_targetfolder_path()

        if target_folder_path is None:
            print(f'No target folder provided. Check setup')
            return

        zipfile_path = os.path.join(target_folder_path, f'xrd_data_collected_on_{datetime_stamp}.zip')
        csv_file_path = os.path.join(target_folder_path,f'xrd_labels_generated_on_{datetime_stamp}.csv')

        print("Checked Paths:", checked_paths)
        try:
            zip_file_list(path_list=checked_paths,
                          zipfile_path=zipfile_path)
            produce_csv_file(absolute_path_list=checked_paths,
                             target_path=csv_file_path)


            self.feedback_widget.text = (f'Wrote {len(checked_paths)} xrd files to .zip file and produced label template at:\n'
                                         f'{zipfile_path} \n'
                                         f'{csv_file_path}')
        except:
            self.feedback_widget.text = f'An error occured during the creating of the zip archive.\nIs "{target_folder_path}" a valid folder path?'
        self.reveal_feedback_text()


    def get_targetfolder_path(self) -> str:
        return self.target_path_input.text if self.targt_folder_override is None else self.targt_folder_override


    def reveal_feedback_text(self):
        self.feedback_widget.opacity = 1
        print(self.feedback_widget.text)


    def get_checked_filepaths(self) -> list[str]:
        all_file_checkboxes = self.root_checkbox.xrd_file_des
        return [box.path for box in all_file_checkboxes if box.get_is_checked()]
