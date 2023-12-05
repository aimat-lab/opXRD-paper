import os
from datetime import datetime
from typing import Optional
from kivy.uix.slider import Slider
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.app import App
from kivy.core.window import Window


from data_collector.filesystem import zip_file_list, produce_csv_file
from elements import PathCheckbox, InputDialog
from elements import get_select_layout, get_scroll_view
from elements import get_file_count_widget, get_ok_button, get_feedback_widget, get_scrollable_checkboxes_layout

# -------------------------------------------

class DataCollectApp(App):
    def __init__(self, target_folder : Optional[str] = None,
                 override_input_folder : Optional[str]  = None):
        super(DataCollectApp, self).__init__()

        # Properties
        self.title : str = 'AiMAT XRD data collect'
        self.target_folder : str = target_folder
        self.input_folder_override : Optional[str]  = override_input_folder
        self.default_font_size = Window.width*0.018

        # PathCheckbox
        self.root_checkbox : Optional[PathCheckbox] = None

        # GUI Elements
        self.slider : Optional[Widget] = None
        self.feedback_widget : Optional[Widget] = None
        self.scroll_view : Optional[Widget] = None
        self.filecount_label : Optional[Widget] = None
        self.input_popup : Optional[Popup] = InputDialog(callback=self.set_select_layout_content)


    def build(self):
        # Main layout
        self.scroll_view = get_scroll_view()

        self.filecount_label = get_file_count_widget(num_elements=0)
        select_layout = get_select_layout(file_count_label=self.filecount_label,
                                          scroll_view=self.scroll_view)
        self.slider = Slider(orientation='vertical',min=0, max=1, value=1, size_hint=(0.1, 1))

        main_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.9))
        main_layout.add_widget(widget=select_layout)
        main_layout.add_widget(widget=self.slider)

        # Finish layout
        ok_button = get_ok_button()
        self.feedback_widget = get_feedback_widget(font_size=self.default_font_size)

        finish_layout = BoxLayout(orientation='horizontal',size_hint =(1,0.1))
        finish_layout.add_widget(ok_button)
        finish_layout.add_widget(self.feedback_widget)

        # Compose
        root_layout = BoxLayout(orientation='vertical')
        root_layout.add_widget(main_layout)
        root_layout.add_widget(finish_layout)

        # Logic
        self.slider.bind(value=self.adjust_scroll_view)
        self.scroll_view.bind(scroll_y=self.on_scroll_view_scroll)
        ok_button.bind(on_press=self.produce_dataset_files)
        Window.bind(size=self.adjust_font_size)

        return root_layout


    def set_select_layout_content(self, path : str):
        self.root_checkbox: PathCheckbox = PathCheckbox(path=path)
        self.root_checkbox.recursively_initialize_descendants()

        new_label = get_file_count_widget(num_elements=len(self.root_checkbox.get_file_descendants()))
        self.filecount_label.text =  new_label.text
        scroll_layout = get_scrollable_checkboxes_layout(root_checkbox=self.root_checkbox)
        self.scroll_view.add_widget(widget=scroll_layout)

    def on_start(self):
        if self.input_folder_override is None:
            self.show_popup()
        else:
            self.set_select_layout_content(path=self.input_folder_override)

    def show_popup(self):
        self.input_popup.open()

    # -------------------------------------------
    # callbacks
    def on_scroll_view_scroll(self, instance, value):
        self.slider.unbind(value=self.adjust_scroll_view)
        self.slider.value = value
        self.slider.bind(value=self.adjust_scroll_view)

    def adjust_font_size(self, instance, value):
        _, __ = instance, value
        self.feedback_widget.font_size = Window.width * self.default_font_size


    def adjust_scroll_view(self, instance, value):
        _ = instance
        self.scroll_view.scroll_y = value


    def produce_dataset_files(self, *args):
        _ = args
        print('Triggered callback of ok button')
        checked_paths = self.get_checked_filepaths()

        current_date = datetime.now()
        datetime_stamp = current_date.strftime('%d_%m_%Y_%H_%M_%S')


        zipfile_path = os.path.join(self.target_folder, f'xrd_data_collected_on_{datetime_stamp}.zip')
        csv_file_path = os.path.join(self.target_folder,f'xrd_labels.csv')

        print("Checked Paths:", checked_paths)
        try:
            zip_file_list(path_list=checked_paths,
                          zipfile_path=zipfile_path)
            produce_csv_file(path_list=checked_paths,
                             target_path=csv_file_path)


            self.feedback_widget.text = (f'Successfully produced zip archive and labels at:\n'
                                         f'{zipfile_path} \n'
                                         f'{csv_file_path}')
        except:
            self.feedback_widget.text = f'An error occured during the creating of the zip archive. Aborting ...'
        self.reveal_feedback_text()

    def reveal_feedback_text(self):
        self.feedback_widget.opacity = 1
        print(self.feedback_widget.text)

    # -------------------------------------------
    # get

    def get_checked_filepaths(self) -> list[str]:
        all_checkboxes = self.root_checkbox.get_file_descendants()
        return [box.path for box in all_checkboxes if box.get_value()]
