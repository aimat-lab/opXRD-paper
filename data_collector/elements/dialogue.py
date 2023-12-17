from __future__ import annotations

import os

from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from data_collector.filesystem import Folder
import platform, sys
# -------------------------------------------

class InputDialog(Popup):
    def __init__(self, callback: callable, **kwargs):
        super(InputDialog, self).__init__(**kwargs)
        self.size_hint = (0.8, 0.6)
        self.title = 'XRD data collector'
        self.title_align = 'center'  # Center the title
        self.auto_dismiss = False  # Disable automatic dismissal of the popup


        self.callback = callback
        # Main container
        self.content = BoxLayout(orientation='vertical', padding=[10, 10, 10, 10], spacing=10)

        # First hint
        first_hint_text = '''This application is designed to scan a given input folder for all xrd formats specified.You can edit this list to your preferences:'''
        self.first_hint = Label(text=first_hint_text,
                                        size_hint=(1, None),
                                        font_size=Window.width * 0.02)
        self.first_hint.bind(width=lambda *x: setattr(self.first_hint, 'text_size', (self.first_hint.width, None)))
        self.first_hint.bind(texture_size=self._update_text_height)


        default_xrd_formats = Folder.default_xrd_formats
        default_xrd_text = ''
        for xrd_format in default_xrd_formats:
            default_xrd_text += f'.{xrd_format},'

        # Input widget
        self.format_input = FocusTextInput(text=f'{default_xrd_text}',
                                      size_hint=(1, 0.08),
                                      font_size=Window.width * 0.02,
                                      multiline=False)

        # Second hint
        second_hint_text = '''Once an input folder is selected, it will be scanned for the specified formats and all xrd files matching that directory will be displayed. You can then check folders or individual files that you want to share. Once you self.confirm that selection, the application will produce a .zip file ready for submission on xrd.aimat.science along with a template .csv file for labels.\n\nEnter file path to "input folder"'''
        self.second_hint = Label(text=second_hint_text,
                                         size_hint=(1, None),
                                         font_size=Window.width * 0.02)
        self.second_hint.bind(width=lambda *x: setattr(self.second_hint, 'text_size', (self.second_hint.width, None)))
        self.second_hint.bind(texture_size=self._update_text_height)

        # Warning label
        self.warning = Label(opacity=0,
                             size_hint=(1, 0.1),
                             halign="left",
                             color=[1, 0, 0, 1])  # RGB for red, and 1 for full opacity


        # Input widget
        self.path_input = FocusTextInput(text=f'{self.get_initial_path()}',
                                    size_hint=(1, 0.08),
                                    font_size=Window.width * 0.02,
                                    multiline=False)

        self.path_input.bind(on_text_validate=self.on_answer)

        # confirm button
        self.confirm = Button(text='confirm', size_hint=(1, 0.08))
        self.confirm.bind(on_press=self.on_answer)

        # Adding widgets to the main container
        self.content.add_widget(self.first_hint)
        self.content.add_widget(self.format_input)
        self.content.add_widget(self.second_hint)
        self.content.add_widget(self.warning)
        self.content.add_widget(self.path_input)
        self.content.add_widget(self.confirm)
        self.set_focus_chain()

    def set_focus_chain(self):
        self.format_input.focus_next = self.path_input
        self.format_input.focus_previous = self.path_input

        self.path_input.focus_next = self.format_input
        self.path_input.focus_previous = self.format_input


    @staticmethod
    def _update_text_height(instance, texture_size):
        instance.height = texture_size[1]  # Set the height to the text height


    def print_warning_notice(self):
        self.warning.text = f'Given input \"{self.path_input.text}\" is not a path to a directory. Please try again'
        self.warning.opacity = 1

    @staticmethod
    def get_initial_path():

        if platform.system() == 'Windows':
            initial_path = os.path.splitdrive(sys.executable)[0] + '\\'
        else:
            initial_path = '/'

        return initial_path

    def on_answer(self, instance):

        Folder.set_default_formats(self.format_input.text)

        _ = instance
        user_input = self.path_input.text

        print(f"User input: {user_input}")
        if not os.path.isdir(user_input):
            self.print_warning_notice()
            self.path_input.text = ''
            return

        self.callback(user_input)
        self.dismiss()


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
