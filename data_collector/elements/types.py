from __future__ import annotations

from kivy.clock import Clock
from kivy.graphics import Color, Line
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.slider import Slider
from kivy.uix.textinput import TextInput

from kivy.uix.image import Image
from kivy.uix.widget import Widget
from data_collector.resources import get_logo_path
from typing import List

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


class Placeholder(Widget):
    def __init__(self, height : int):
        super().__init__(size_hint=(1, None), size=(height, height))




class HeaderWidget(BoxLayout):
    def __init__(self, num_elements: int, format_list : List[str]):
        super().__init__(orientation='horizontal', size_hint=(1, 0.125))
        with_leading_dot_list = [f'.{the_format}' for the_format in format_list]

        file_count_label = BlackLabel(
            text=f"Found {num_elements} files that match specified XRD formats:\n {with_leading_dot_list}",
            size_hint=(0.6, 1),  # Adjusted size hint
            halign="center",
            valign="middle"
        )
        file_count_label.bind(size=file_count_label.setter('text_size'))

        logo_image = Image(source=get_logo_path(), size_hint=(0.3, 1))

        left_placeholder = Widget(size_hint=(0.4, 1))
        right_placeholder = Widget(size_hint=(0.1, 1))

        self.add_widget(left_placeholder)  # Placeholder to balance the self
        self.add_widget(file_count_label)
        self.add_widget(right_placeholder)  # Placeholder to balance the self
        self.add_widget(logo_image)
