from __future__ import annotations

import os
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget

from data_collector.elements.types import BlackLabel

# -------------------------------------------

class FinishLayout(BoxLayout):
    def __init__(self, callback: callable, **kwargs):
        super(FinishLayout, self).__init__(orientation='vertical', size_hint=(1, 0.14*0.5),padding=(0, 10, 0, 10),**kwargs)
        upper_finish = BoxLayout(orientation='horizontal', size_hint=(1, 0.3),spacing=10)

        note = BlackLabel(text='Target folder:', size_hint=(0.2, 1), font_size=Window.width * 0.02, bold=True)


        self.target_path_input = TextInput(text=f'{os.getcwd()}',
                                           size_hint=(0.7, 1),
                                           font_size=Window.width * 0.02,
                                           multiline=False)
        buffer = BlackLabel(text='', size_hint=(0.075, 1))

        ok_button = self.get_ok_button()
        ok_button.bind(on_press=callback)

        upper_finish.add_widget(note)
        upper_finish.add_widget(self.target_path_input)
        upper_finish.add_widget(ok_button)
        upper_finish.add_widget(buffer)

        # lower_finish = BoxLayout(orientation='horizontal', size_hint=(1, 0.6))

        self.default_font_size = Window.width * 0.016
        self.feedback_widget = self.get_feedback_widget(font_size=self.default_font_size)
        # lower_finish.add_widget(self.feedback_widget)

        self.add_widget(upper_finish)
        # self.add_widget(lower_finish)

    @staticmethod
    def get_feedback_widget(font_size: float) -> Widget:
        return BlackLabel(size_hint=(0.8, 1),
                          opacity=0,
                          font_size=font_size)

    @staticmethod
    def get_ok_button() -> Widget:
        ok_button = Button(text="OK", size_hint=(0.2, 1))
        ok_button.background_color = (0, 1, 0, 1)  # (R, G, B, A)
        return ok_button
