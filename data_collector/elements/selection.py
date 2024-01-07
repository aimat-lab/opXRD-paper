from __future__ import annotations

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView

from data_collector.elements.types import BlackLabel
from data_collector.elements.path_checkbox import PathCheckbox
from data_collector.filesystem.fsnode import FsNode

from kivy.uix.widget import Widget


# -------------------------------------------
# widgets

def get_file_count_widget(num_elements: int) -> Widget:

    with_leading_dot_list = [f'.{xrd_format}' for xrd_format in FsNode.default_xrd_formats]

    file_count_label = BlackLabel(
        text=f"Found {num_elements} files that match specified XRD formats:\n {with_leading_dot_list}" ,
        size_hint=(1, 0.15),
        halign="center",  # Horizontally center the text
        valign="middle"  # Vertically center the text
    )
    file_count_label.bind(size=file_count_label.setter('text_size'))  # Bind the text size to the label size
    return file_count_label


def get_feedback_widget(font_size : float) -> Widget:
    return BlackLabel(size_hint=(0.8, 1),
                      opacity=0,
                      font_size=font_size)


def get_ok_button() -> Widget:
    ok_button = Button(text="OK", size_hint=(0.2, 1))
    return ok_button


# -------------------------------------------
# layouts

def get_checkboxes_layout(file_count_label: Label, scroll_view: ScrollView):
    select_layout = BoxLayout(orientation='vertical')
    select_layout.add_widget(widget=file_count_label)
    select_layout.add_widget(widget=scroll_view)

    return select_layout


def get_scroll_view():
    scroll_view = ScrollView(size_hint=(1, 1), bar_width=0)
    return scroll_view


def get_scrollable_checkboxes_layout(root_checkbox : PathCheckbox):
    scroll_layout = BoxLayout(orientation='vertical', size_hint_y=None)
    scroll_layout.bind(minimum_height=scroll_layout.setter('height'))
    recursively_add_boxes(gui_parent=scroll_layout, root_box=root_checkbox, indent=0)

    return scroll_layout


def recursively_add_boxes(gui_parent, root_box : PathCheckbox, indent : int):
    if not root_box.get_is_file() and len(root_box.xrd_file_des) == 0:
        return

    root_box.initialize_gui(gui_parent, level=indent)

    for child_box in root_box.active_children:
        recursively_add_boxes(gui_parent=root_box.child_container,
                              root_box=child_box,
                              indent=indent + 1)
