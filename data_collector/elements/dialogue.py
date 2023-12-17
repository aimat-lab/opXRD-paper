from __future__ import annotations

import os

from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput

from data_collector.elements.selection_widgets import AutoSizeLabel
# from data_collector.filesystem import Folder

# -------------------------------------------

class InputDialog(Popup):
    def __init__(self, callback: callable, **kwargs):
        super(InputDialog, self).__init__(**kwargs)
        self.size_hint = (0.8, 0.6)
        self.title = 'XRD data collector'
        self.callback = callback

        # Main container
        self.content = BoxLayout(orientation='vertical', size_hint=(1, 1))

        # First hint
        first_hint_text = '''This application is designed to scan a given input folder for all xrd formats specified. You edit this list to your preferences.'''
        self.first_hint = AutoSizeLabel(text=first_hint_text,
                                        size_hint=(1, None),
                                        font_size=Window.width * 0.02)
        self.first_hint.bind(width=lambda *x: setattr(self.first_hint, 'text_size', (self.first_hint.width, None)))

        # Second hint
        second_hint_text = '''Once an input folder is selected, it will be scanned for the specified formats and all xrd files matching that directory will be displayed. You can then check folders or individual files that you want to share. Once you confirm that selection, the application will produce a .zip file ready for submission on xrd.aimat.science along with a template .csv file for labels.\n\nEnter file path to "input folder"'''
        self.second_hint = AutoSizeLabel(text=second_hint_text,
                                         size_hint=(1, None),
                                         font_size=Window.width * 0.02)
        self.second_hint.bind(width=lambda *x: setattr(self.second_hint, 'text_size', (self.second_hint.width, None)))

        # Warning label
        self.warning = Label(opacity=0,
                             size_hint=(1, 0.1),
                             halign="left")

        # Input widget
        self.input_widget = TextInput(text='',
                                      size_hint=(1, 0.025),
                                      font_size=Window.width * 0.02,
                                      multiline=False)
        self.input_widget.bind(on_text_validate=self.on_answer)

        # Confirm button
        confirm = Button(text='Confirm', size_hint=(1, 0.025))
        confirm.bind(on_press=self.on_answer)

        # Adding widgets to the main container
        self.content.add_widget(self.first_hint)
        self.content.add_widget(self.second_hint)
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
