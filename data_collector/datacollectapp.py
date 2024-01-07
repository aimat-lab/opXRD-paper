import os
from datetime import datetime
from typing import Optional
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.textinput import TextInput

from data_collector.filesystem import zip_file_list, produce_csv_file, get_initial_path
from data_collector.elements import PathCheckbox, InputDialog, BlackLabel, ThickVerticalSlider, get_checkboxes_layout, \
    get_scroll_view, get_scrollable_checkboxes_layout
from data_collector.elements import get_file_count_widget, get_ok_button, get_feedback_widget
from data_collector.configs import get_line_height


# -------------------------------------------

class DataCollectApp(App):
    def __init__(self, override_input_folder : Optional[str]  = None):
        self.icon = None    
        super(DataCollectApp, self).__init__()

        # Properties
        self.title : str = 'AiMAT XRD data collect'
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
        self.target_path_input : Optional[Widget] = None

    def build(self):
        # Main layout
        self.scroll_view = get_scroll_view()
        scrol_unit = 200
        self.scroll_view.scroll_distance = scrol_unit
        self.scroll_view.scroll_wheel_distance = scrol_unit

        self.filecount_label = get_file_count_widget(num_elements=0)
        self.filecount_label.opacity = 0

        checkboxes_layout = get_checkboxes_layout(file_count_label=self.filecount_label,
                                                  scroll_view=self.scroll_view)
        self.slider = ThickVerticalSlider(orientation='vertical', min=0, max=1, value=1, size_hint=(0.1, 1))

        selection_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.9))
        selection_layout.add_widget(widget=checkboxes_layout)
        selection_layout.add_widget(widget=self.slider)

        # Finish layout
        ok_button = get_ok_button()
        self.feedback_widget = get_feedback_widget(font_size=self.default_font_size)

        finish_layout = BoxLayout(orientation='vertical',size_hint =(1,0.125))
        upper_finish = BoxLayout(orientation='horizontal', size_hint=(1, 0.4))

        # Add an explanatory note
        note = BlackLabel(text='Target folder:',size_hint=(0.2,1))

        self.target_path_input = TextInput(text=f'{os.getcwd()}',
                                    size_hint=(0.8, 1),
                                    font_size=Window.width * 0.02,
                                    multiline=False)

        upper_finish.add_widget(note)
        upper_finish.add_widget(self.target_path_input)

        lower_finish = BoxLayout(orientation='horizontal',size_hint =(1,0.6))
        lower_finish.add_widget(ok_button)
        lower_finish.add_widget(self.feedback_widget)

        finish_layout.add_widget(upper_finish)
        finish_layout.add_widget(lower_finish)

        # Compose
        root_layout = BoxLayout(orientation='vertical')
        root_layout.add_widget(selection_layout)
        root_layout.add_widget(finish_layout)

        # Logic
        self.slider.bind(value=self.adjust_scroll_view)
        self.scroll_view.bind(scroll_y=self.on_scroll_view_scroll)
        ok_button.bind(on_press=self.produce_dataset_files)
        Window.bind(size=self.adjust_font_size)

        return root_layout


    def set_select_layout_content(self, path : str):
        self.root_checkbox: PathCheckbox = PathCheckbox(path=path, height=get_line_height(), scroll_view=self.scroll_view)
        self.root_checkbox.recursively_initialize_descendants()

        new_label = get_file_count_widget(num_elements=len(self.root_checkbox.get_file_descendants()))
        self.filecount_label.text =  new_label.text
        self.filecount_label.opacity = 1

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
        _ = instance
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

        target_folder = self.target_path_input.text

        if target_folder is None:
            print(f'No target folder provided. Check setup')
            return

        zipfile_path = os.path.join(target_folder, f'xrd_data_collected_on_{datetime_stamp}.zip')
        csv_file_path = os.path.join(target_folder,f'xrd_labels_generated_on_{datetime_stamp}.csv')

        print("Checked Paths:", checked_paths)
        try:
            zip_file_list(path_list=checked_paths,
                          zipfile_path=zipfile_path)
            produce_csv_file(path_list=checked_paths,
                             target_path=csv_file_path)


            self.feedback_widget.text = (f'Wrote {len(checked_paths)} xrd files to .zip file and produced label template at:\n'
                                         f'{zipfile_path} \n'
                                         f'{csv_file_path}')
        except:
            self.feedback_widget.text = f'An error occured during the creating of the zip archive. Aborting ...'
        self.reveal_feedback_text()

    def reveal_feedback_text(self):
        self.feedback_widget.opacity = 1
        print(self.feedback_widget.text)


    # -------------------------------------------
    # other

    def get_checked_filepaths(self) -> list[str]:
        all_checkboxes = self.root_checkbox.get_file_descendants()
        return [box.path for box in all_checkboxes if box.get_value()]
