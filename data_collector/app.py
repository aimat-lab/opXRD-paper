import os
from datetime import datetime
from typing import Optional
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.textinput import TextInput

from data_collector.filesystem import zip_file_list, produce_csv_file
from data_collector.elements import NodeWidget, InputDialog, BlackLabel, ThickVerticalSlider, get_checkboxes_layout, \
    get_scroll_view, get_scrollable_checkboxes_layout
from data_collector.elements import get_header_widget, get_ok_button, get_feedback_widget
from data_collector.configs import get_line_height


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

        # GUI Elements
        self.slider : Optional[Widget] = None
        self.feedback_widget : Optional[Widget] = None
        self.scroll_view : Optional[Widget] = None
        self.header_layout : Optional[Widget] = None
        self.target_path_input : Optional[Widget] = None


    def build(self):
        self.scroll_view = get_scroll_view()
        self.scroll_view.bind(scroll_y=self.on_scroll_view_scroll)

        selection_layout = self.make_selection_layout()
        finish_layout = self.make_finish_layout()

        root_layout = BoxLayout(orientation='vertical')
        root_layout.add_widget(selection_layout)
        root_layout.add_widget(finish_layout)

        return root_layout


    def make_selection_layout(self):
        self.header_layout = get_header_widget(num_elements=0)
        self.header_layout.opacity = 0
        checkboxes_layout = get_checkboxes_layout(file_count_label=self.header_layout,
                                                  scroll_view=self.scroll_view)
        self.slider = ThickVerticalSlider(orientation='vertical', min=0, max=1, value=1, size_hint=(0.1, 1))
        self.slider.bind(value=self.adjust_scroll_view)

        selection_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.9))
        selection_layout.add_widget(widget=checkboxes_layout)
        selection_layout.add_widget(widget=self.slider)

        return selection_layout


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

    def set_select_layout_content(self, path : str):
        self.root_checkbox: NodeWidget = NodeWidget(path=path, height=get_line_height(), scroll_view=self.scroll_view)
        self.root_checkbox.recursively_initialize_filestructure()

        new_label = get_header_widget(num_elements=len(self.root_checkbox.xrd_file_des)).children[2]
        self.header_layout.children[2].text =  new_label.text
        self.header_layout.opacity = 1

        scroll_layout = get_scrollable_checkboxes_layout(root_checkbox=self.root_checkbox)
        self.scroll_view.add_widget(widget=scroll_layout)


    def on_start(self):
        if self.input_folder_override is None:
            self.show_launch_dialog(callback=self.set_select_layout_content)
        else:
            self.set_select_layout_content(path=self.input_folder_override)

    @staticmethod
    def show_launch_dialog( callback : callable):
        InputDialog(callback=callback).open()

    # -------------------------------------------
    # callbacks
    def on_scroll_view_scroll(self, instance, value):
        _ = instance
        self.slider.unbind(value=self.adjust_scroll_view)
        self.slider.value = value
        self.slider.bind(value=self.adjust_scroll_view)


    def adjust_scroll_view(self, instance, value):
        _ = instance
        self.scroll_view.scroll_y = value


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
