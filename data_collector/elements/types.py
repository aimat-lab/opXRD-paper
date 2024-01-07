from __future__ import annotations

from kivy.uix.textinput import TextInput


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
