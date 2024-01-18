from __future__ import annotations

from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout

from kivy.uix.checkbox import CheckBox
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.togglebutton import ToggleButton

from data_collector.configs import get_line_height
from data_collector.elements.types import BlackLabel

from data_collector.resources import get_unchecked_box_path, get_checked_box_path, get_fileicon_path, \
    get_foldericon_path, get_collapsed_icon_path, get_expanded_icon_path

# -------------------------------------------

class NodeWidget(BoxLayout):
    def __init__(self, callback : callable, height : int, labeled_checkbox : LabeledCheckBox, is_file : bool):
        super().__init__(orientation='horizontal', size_hint=(1, None))

        if not is_file:
            icon_toggle_button = IconToggleButton(size_hint=(None, None),
                                          size=(height,height))

            icon_toggle_button.btn.bind(state=callback)
            self.add_widget(icon_toggle_button)
        else:
            place_holder = Label(size_hint=(None,None),size=(height,height))
            self.add_widget(place_holder)

        self.add_widget(labeled_checkbox)
        self.bind(minimum_height=self.setter('height'))


class LabeledCheckBox(BoxLayout):
    indent = get_line_height()*1.5

    def __init__(self, height : int, text :str, check_callback, is_file : bool, indent=0, **kwargs):
        super().__init__(**kwargs)
        self.size_hint_y = None
        self.height = height

        self.check_box = ImageCheckBox(size_hint=(None, None), size=(self.height, self.height))
        self.check_box.bind(active=check_callback)

        icon_path = get_fileicon_path() if is_file else get_foldericon_path()
        self.icon = Image(source=icon_path, size_hint=(None, None), size=(self.height, self.height))
        self.add_widget(self.icon)


        self.label = BlackLabel(text=text,
                                font_size=Window.width * 0.018,
                                size_hint_x=None,
                                size_hint_y=1,
                                halign='left',
                                valign='middle')

        self.add_widget(self.check_box)
        self.add_widget(self.label)
        self.padding = [indent * LabeledCheckBox.indent, 0, 0, 0]  # Left padding for indentation


class IconToggleButton(RelativeLayout):
    def __init__(self, **kwargs):
        super(IconToggleButton, self).__init__(**kwargs)

        height = self.height
        self.collapsed = Image(source=get_collapsed_icon_path(), size_hint=(None, None),size=(height,height))
        self.expanded = Image(source=get_expanded_icon_path(), size_hint=(None, None),size=(height,height))

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
