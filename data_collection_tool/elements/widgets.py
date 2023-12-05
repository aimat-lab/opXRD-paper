from __future__ import annotations
import os

from PIL import Image
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.checkbox import CheckBox
from kivy.uix.image import Image
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.core.window import Window
from data_collector.filesystem import Folder
from kivy.uix.scrollview import ScrollView

from data_collector.resources import get_foldericon_path,get_fileicon_path
# -------------------------------------------
from data_collector.resources import get_collapsed_icon_path, get_expanded_icon_path

class LabeledCheckBox(BoxLayout):
    indent = 50

    def __init__(self, text, toggle_callback, is_file : bool, indent=0, **kwargs):
        super().__init__(**kwargs)
        # Properties
        self.size_hint_y = None
        self.height = 30  # Fixed height for each LabeledCheckBox

        # Create the CheckBox
        self.check_box = CheckBox(size_hint=(None, None), size=(30, 30))
        self.check_box.bind(active=toggle_callback)

        # Create the Icon
        icon_path = get_fileicon_path() if is_file else get_foldericon_path()
        self.icon = Image(source=icon_path, size_hint=(None, None), size=(30, 30))
        self.add_widget(self.icon)

        # Create the Label
        self.label = BlackLabel(text=text,
                                size_hint_x=None,
                                size_hint_y=None,
                                height=30,
                                halign='left',
                                valign='middle')

        self.add_widget(self.check_box)
        self.add_widget(self.label)
        self.padding = [indent * LabeledCheckBox.indent, 0, 0, 0]  # Left padding for indentation


class InputDialog(Popup):
    def __init__(self, callback  : callable, **kwargs):
        super(InputDialog, self).__init__(**kwargs)
        self.size_hint = (0.8, 0.6)
        self.title = 'XRD data collector'
        self.callback = callback

        self.scroll_view = ScrollView(size_hint=(1, 0.8))
        self.hint = AutoSizeLabel(text='This application is designed to scan a given input folder for all files that fit any of the following common XRD formats: '
                                    f'{Folder.xrd_formats}\n\n'
                                    'Once an input folder is selected, you will be presented with a view that displays all xrd files found in the input directory '
                                    'and all subdirectories and allow for a selection of what files you want to share. Once you confirm that selection, the application will produce a .zip '
                                    'file ready for submission along with a template .csv file for labels \n\n'
                                    'Enter file path to \"input folder\"',
                                     size_hint=(1, None))
        self.hint.bind(width=lambda *x: setattr(self.hint, 'text_size', (self.hint.width, 0.8*self.height)))
        self.warning = Label(opacity=0,
                             size_hint = (1, 0.1),
                             halign="left")

        # Adding BlackLabel to ScrollView
        self.scroll_view.add_widget(self.hint)
        self.input_widget = TextInput(text='',
                                    size_hint=(1, 0.125),
                                    font_size=Window.width * 0.02)

        confirm = Button(text='Confirm', size_hint=(1, 0.1))
        confirm.bind(on_press=self.on_answer)

        self.content = BoxLayout(orientation='vertical')

        self.content.add_widget(self.scroll_view)
        self.content.add_widget(self.warning)
        self.content.add_widget(self.input_widget)
        self.content.add_widget(confirm)


    def print_warning_notice(self):
        self.warning.text = f'Given input \"{self.input_widget.text}\" is not a path to a directory. Please try again'
        self.warning.opacity = 1

    def on_answer(self, instance):
        _ = instance
        user_input = self.input_widget.text

        print(f"User input: {user_input}")
        if not os.path.isdir(user_input):
            self.print_warning_notice()
            self.input_widget.text = ''
            return

        self.callback(user_input)
        self.dismiss()



class ImageToggleButton(RelativeLayout):
    def __init__(self, **kwargs):
        super(ImageToggleButton, self).__init__(**kwargs)

        self.collapsed = Image(source=get_collapsed_icon_path(), size_hint=(None, None),size=(30,30))
        self.expanded = Image(source=get_expanded_icon_path(), size_hint=(None, None),size=(30,30))

        self.toggle_button = ToggleButton(size_hint=(1, 1), background_color=(0, 0, 0, 0))
        self.add_widget(self.toggle_button)

        self.icon = self.collapsed if self.toggle_button.state == 'down' else self.expanded
        self.add_widget(self.icon)

        self.toggle_button.bind(state=self.toggle_image)


    def toggle_image(self,instance, value):
        self.remove_widget(self.icon)
        if value == 'down':
            self.icon = self.collapsed
        else:
            self.icon = self.expanded
        self.add_widget(self.icon)


class AutoSizeLabel(Label):
    def __init__(self, text: str = '', *args, **kwargs):
        _ = args
        super().__init__(**kwargs,text=text)
        # self.set_label_width()

        if not 'size_hint' in kwargs and not 'size' in kwargs:
            Clock.schedule_once(lambda dt: self.set_label_size())


    def set_label_size(self):
        self.width = self.texture_size[0]
        self.height = self.texture_size[1]
        self.text_size = (self.width, self.height)


class BlackLabel(AutoSizeLabel):
    def __init__(self, text: str = '', *args, **kwargs):
        _ = args
        kwargs.setdefault('color',(0,0,0,1))
        super().__init__(**kwargs, text=text)



def get_file_count_widget(num_elements: int):
    file_count_label = BlackLabel(
        text=f"Found {num_elements} files that match XRD formats",
        size_hint=(1, None),
        halign="center",  # Horizontally center the text
        valign="middle"  # Vertically center the text
    )
    file_count_label.bind(size=file_count_label.setter('text_size'))  # Bind the text size to the label size
    return file_count_label


def get_feedback_widget(font_size : float):
    return BlackLabel(size_hint=(0.8, 1),
                      opacity=0,
                      font_size=font_size)


def get_ok_button():
    ok_button = Button(text="OK", size_hint=(0.2, 1))
    return ok_button


