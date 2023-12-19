from __future__ import annotations

from PIL import Image
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.checkbox import CheckBox
from kivy.uix.image import Image
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.label import Label
from kivy.uix.button import Button

from kivy.app import App
from kivy.uix.slider import Slider
from kivy.graphics import Color, Line

from data_collector.filesystem.folder import Folder
from data_collector.resources import get_foldericon_path,get_fileicon_path
# -------------------------------------------
from data_collector.resources import get_collapsed_icon_path, get_expanded_icon_path

class LabeledCheckBox(BoxLayout):
    indent = 50

    def __init__(self, height : int, text :str, toggle_callback, is_file : bool, indent=0, **kwargs):
        super().__init__(**kwargs)
        # Properties
        self.size_hint_y = None
        self.height = height

        # Create the CheckBox
        self.check_box = CheckBox(size_hint=(None, None), size=(self.height, self.height))
        self.check_box.bind(active=toggle_callback)

        # Create the Icon
        icon_path = get_fileicon_path() if is_file else get_foldericon_path()
        self.icon = Image(source=icon_path, size_hint=(None, None), size=(self.height, self.height))
        self.add_widget(self.icon)

        # Create the Label
        self.label = BlackLabel(text=text,
                                size_hint_x=None,
                                size_hint_y=None,
                                halign='left',
                                valign='middle')

        self.add_widget(self.check_box)
        self.add_widget(self.label)
        self.padding = [indent * LabeledCheckBox.indent, 0, 0, 0]  # Left padding for indentation


class ImageToggleButton(RelativeLayout):
    def __init__(self, **kwargs):
        super(ImageToggleButton, self).__init__(**kwargs)

        self.collapsed = Image(source=get_collapsed_icon_path(), size_hint=(None, None),size=(self.height,self.height))
        self.expanded = Image(source=get_expanded_icon_path(), size_hint=(None, None),size=(self.height,self.height))

        self.toggle_button = ToggleButton(size_hint=(1, 1), background_color=(0, 0, 0, 0))
        self.add_widget(self.toggle_button)

        self.icon = self.collapsed if self.toggle_button.state == 'down' else self.expanded
        self.add_widget(self.icon)

        self.toggle_button.bind(state=self.toggle_image)


    def toggle_image(self,instance, value):
        _ = instance
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

    with_leading_dot_list = [f'.{xrd_format}' for xrd_format in Folder.default_xrd_formats]

    file_count_label = BlackLabel(
        text=f"Found {num_elements} files that match specified XRD formats:\n {with_leading_dot_list}" ,
        size_hint=(1, 0.15),
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




class ThickVerticalSlider(Slider):
    def __init__(self, **kwargs):
        super(ThickVerticalSlider, self).__init__(**kwargs)
        self.bind(pos=self._update_canvas, size=self._update_canvas)

    def _update_canvas(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(0.5, 0.5, 0.5, 1)  # Grey color for the track
            line_width = 2  # Adjust width for thickness
            Line(points=[self.x + self.width / 2, self.y + line_width / 2,
                         self.x + self.width / 2, self.y + self.height - line_width / 2],
                 width=line_width)