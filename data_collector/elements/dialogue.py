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
from data_collector.filesystem import Folder

# -------------------------------------------

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
                                     size_hint=(1, None),
                                     font_size=Window.width * 0.02)
        self.hint.bind(width=lambda *x: setattr(self.hint, 'text_size', (self.hint.width, 0.8*self.height)))
        self.warning = Label(opacity=0,
                             size_hint = (1, 0.1),
                             halign="left")

        # Adding BlackLabel to ScrollView
        self.scroll_view.add_widget(self.hint)
        self.input_widget = TextInput(text='',
                                    size_hint=(1, 0.1),
                                    font_size=Window.width * 0.02,
                                      multiline=False)
        self.input_widget.bind(on_text_validate=self.on_answer)

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
