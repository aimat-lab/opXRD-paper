import os
from datetime import datetime
from typing import Optional
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App

from data_collector.filesystem import zip_file_list, produce_csv_file
from data_collector.elements import InputDialog
from data_collector.elements import SelectionLayout, FinishLayout


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


        # PathCheckbox
        self.selection_layout : Optional[SelectionLayout] = None
        self.finish_layout : Optional[FinishLayout] = None


    def on_start(self):
        if self.input_folder_override is None:
            self.show_launch_dialog(callback=self.selection_layout.set_content)
        else:
            self.selection_layout.set_content(path=self.input_folder_override)

    @staticmethod
    def show_launch_dialog( callback : callable):
        InputDialog(callback=callback).open()


    def build(self):
        self.selection_layout = SelectionLayout()
        self.finish_layout = FinishLayout(callback=self.produce_dataset_files)

        root_layout = BoxLayout(orientation='vertical')
        root_layout.add_widget(self.selection_layout)
        root_layout.add_widget(self.finish_layout)

        return root_layout

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
                          zipfile_path=zipfile_path,
                          root_path=self.get_rootfolder_path())
            produce_csv_file(absolute_path_list=checked_paths,
                             target_path=csv_file_path,
                             root_path=self.get_rootfolder_path())


            self.finish_layout.feedback_widget.text = (f'Wrote {len(checked_paths)} xrd files to .zip file and produced label template at:\n'
                                         f'{zipfile_path} \n'
                                         f'{csv_file_path}')
        except:
            self.finish_layout.feedback_widget.text = f'An error occured during the creating of the zip archive.\nIs "{target_folder_path}" a valid folder path?'
        self.reveal_feedback_text()


    def get_checked_filepaths(self) -> list[str]:
        all_file_checkboxes = self.selection_layout.root_checkbox.get_xrd_file_des()
        return [box.path for box in all_file_checkboxes if box.get_is_checked()]


    def get_rootfolder_path(self) -> str:
        return self.selection_layout.root_checkbox.path

    def get_targetfolder_path(self) -> str:
        return self.finish_layout.target_path_input.text if self.targt_folder_override is None else self.targt_folder_override


    def reveal_feedback_text(self):
        self.finish_layout.feedback_widget.opacity = 1
        print(self.finish_layout.feedback_widget.text)

