from __future__ import annotations

from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics import Color, Line
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.slider import Slider
from kivy.uix.togglebutton import ToggleButton

from kivy.uix.textinput import TextInput

from data_collector.resources import get_fileicon_path, get_foldericon_path, get_collapsed_icon_path, \
    get_expanded_icon_path, get_unchecked_box_path, get_checked_box_path


class FocusTextInput(TextInput):
    def keyboard_on_key_down(self, window, keycode, text, modifiers):
        if keycode[1] == 'tab':  # Check if the key is Tab
            if 'shift' in modifiers:  # Check if Shift is also pressed
                # Focus the previous widget
                if self.focus_previous:
                    self.focus_previous.focus = True
            else:
                # Focus the next widget
                if self.focus_next:
                    self.focus_next.focus = True
            return True  # Indicate that the key was handled
        return super(FocusTextInput, self).keyboard_on_key_down(window, keycode, text, modifiers)


class LabeledCheckBox(BoxLayout):
    indent = 50

    def __init__(self, height : int, text :str, check_callback, is_file : bool, indent=0, **kwargs):
        super().__init__(**kwargs)
        # Properties
        self.size_hint_y = None
        self.height = height

        # Create the CheckBox
        self.check_box = ImageCheckBox(size_hint=(None, None), size=(self.height, self.height))
        self.check_box.bind(active=check_callback)

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


class IconToggleButton(RelativeLayout):
    def __init__(self, **kwargs):
        super(IconToggleButton, self).__init__(**kwargs)

        self.collapsed = Image(source=get_collapsed_icon_path(), size_hint=(None, None),size=(self.height,self.height))
        self.expanded = Image(source=get_expanded_icon_path(), size_hint=(None, None),size=(self.height,self.height))

        self.btn = ToggleButton(size_hint=(1, 1), background_color=(0, 0, 0, 0))
        self.add_widget(self.btn)

        self.icon = self.collapsed if self.btn.state == 'down' else self.expanded
        self.add_widget(self.icon)

        self.btn.bind(state=self.toggle_image)


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


class ImageCheckBox(CheckBox):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._checkbox_image = get_unchecked_box_path()

    def on_state(self, widget, value):
        _ = widget
        if value == 'down':
            self._checkbox_image = get_checked_box_path()
        else:
            self._checkbox_image = get_unchecked_box_path()


class ThickVerticalSlider(Slider):
    def __init__(self, **kwargs):
        super(ThickVerticalSlider, self).__init__(**kwargs)
        self.bind(pos=self._update_canvas, size=self._update_canvas)

    def _update_canvas(self, *args):
        _ = args
        self.canvas.before.clear()
        with self.canvas.before:
            Color(0.5, 0.5, 0.5, 1)  # Grey color for the track
            line_width = 2  # Adjust width for thickness
            Line(points=[self.x + self.width / 2, self.y + line_width / 2,
                         self.x + self.width / 2, self.y + self.height - line_width / 2],
                 width=line_width)
