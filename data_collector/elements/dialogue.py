from __future__ import annotations

import os

from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup

from data_collector.elements.types import FocusTextInput
from data_collector.filesystem import Folder, get_initial_path
# -------------------------------------------

class InputDialog(Popup):
    def __init__(self, callback: callable, **kwargs):
        super(InputDialog, self).__init__(**kwargs)
        self.size_hint = (0.8, 0.6)
        self.title = 'XRD data collector'
        self.title_align = 'center'
        self.auto_dismiss = False
        self.callback = callback
        self.content = BoxLayout(orientation='vertical', padding=[10, 10, 10, 10], spacing=10)

        first_hint = self.make_hint()
        self.format_input =self.make_format_input()
        second_hint = self.make_second_hint()

        self.notice = self.make_notice()
        self.path_input = self.make_path_input()
        confirm_button = self.make_confirm_button()

        # Adding widgets to the main container
        self.content.add_widget(first_hint)
        self.content.add_widget(self.format_input)
        self.content.add_widget(second_hint)
        self.content.add_widget(self.notice)
        self.content.add_widget(self.path_input)
        self.content.add_widget(confirm_button)
        self.set_focus_chain()

    def set_focus_chain(self):
        self.format_input.focus_next = self.path_input
        self.format_input.focus_previous = self.path_input

        self.path_input.focus_next = self.format_input
        self.path_input.focus_previous = self.format_input


    # -------------------------------------------
    # Callbacks

    @staticmethod
    def _update_text_height(instance, texture_size):
        instance.height = texture_size[1]  # Set the height to the text height

    def on_confirm(self, instance):
        Folder.set_default_formats(self.format_input.text)

        _ = instance
        user_input = self.path_input.text

        print(f"User input: {user_input}")
        if not os.path.isdir(user_input):
            self.print_warning()
            self.path_input.text = ''
            return
        else:
            self.print_wait()


        Clock.schedule_once(lambda dt: self.callback(user_input),0.1)
        self.dismiss()

    def print_warning(self):
        self.notice.text = f'Given input \"{self.path_input.text}\" is not a path to a directory. Please try again'
        self.notice.opacity = 1

    def print_wait(self):
        self.notice.text = f'Generating selection. Please wait ...'
        self.notice.opacity = 1
        self.notice.color = [0,1,0,1]


    # -------------------------------------------
    # make widgets

    def make_hint(self) -> Widget:
        first_hint_text = '''This application is designed to scan a given input folder for all xrd formats specified.You can edit this list to your preferences:'''
        hint = Label(text=first_hint_text,
                          size_hint=(1, None),
                          font_size=Window.width * 0.02)
        hint.bind(width=lambda *x: setattr(hint, 'text_size', (hint.width, None)))
        hint.bind(texture_size=self._update_text_height)

        return hint


    def make_second_hint(self) -> Widget:
        second_hint_text = '''Once an input folder is selected, it will be scanned for the specified formats and all xrd files matching that directory will be displayed. You can then check folders or individual files that you want to share. Once you confirm that selection, the application will produce a .zip file ready for submission on xrd.aimat.science along with a template .csv file for labels.\n\nEnter file path to "input folder"'''
        second_hint = Label(text=second_hint_text,
                                         size_hint=(1, None),
                                         font_size=Window.width * 0.02)
        second_hint.bind(width=lambda *x: setattr(second_hint, 'text_size', (second_hint.width, None)))
        second_hint.bind(texture_size=self._update_text_height)

        return second_hint


    @staticmethod
    def make_format_input() -> Widget:
        default_xrd_formats = Folder.default_xrd_formats
        default_xrd_text = ''
        for xrd_format in default_xrd_formats:
            default_xrd_text += f'.{xrd_format},'

        format_input = FocusTextInput(text=f'{default_xrd_text}',
                                           size_hint=(1, 0.08),
                                           font_size=Window.width * 0.02,
                                           multiline=False)
        return format_input


    @staticmethod
    def make_notice() -> Widget:
        return Label(opacity=0,
                     size_hint=(1, 0.1),
                     halign="left",
                     color=[1, 0, 0, 1])


    def make_path_input(self) -> Widget:
        path_input = FocusTextInput(text=f'{get_initial_path()}',
                                         size_hint=(1, 0.08),
                                         font_size=Window.width * 0.02,
                                         multiline=False)

        path_input.bind(on_text_validate=self.on_confirm)
        return path_input


    def make_confirm_button(self) -> Widget:
        confirm = Button(text='confirm', size_hint=(1, 0.08))
        confirm.bind(on_press=self.on_confirm)
        return confirm
