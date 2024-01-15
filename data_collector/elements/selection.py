from __future__ import annotations

# from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView

from data_collector.elements.types import BlackLabel
from data_collector.elements.fsnode_widget import NodeWidget
from data_collector.filesystem.fsnode import FsNode

# from kivy.uix.widget import Widget

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.widget import Widget

from data_collector.resources import get_logo_path

# -------------------------------------------
# widgets

def get_header_widget(num_elements: int) -> Widget:
    with_leading_dot_list = [f'.{xrd_format}' for xrd_format in FsNode.default_xrd_formats]

    file_count_label = BlackLabel(
        text=f"Found {num_elements} files that match specified XRD formats:\n {with_leading_dot_list}",
        size_hint=(0.6, 1),  # Adjusted size hint
        halign="center",
        valign="middle"
    )
    file_count_label.bind(size=file_count_label.setter('text_size'))

    logo_image = Image(source=get_logo_path(), size_hint=(0.3, 1))

    # Transparent placeholders to center the logo
    left_placeholder = Widget(size_hint=(0.4, 1))
    right_placeholder = Widget(size_hint=(0.1, 1))

    layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.125))
    layout.add_widget(left_placeholder)  # Placeholder to balance the layout
    layout.add_widget(file_count_label)
    layout.add_widget(right_placeholder)  # Placeholder to balance the layout
    layout.add_widget(logo_image)

    return layout


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
    scrol_unit = 200
    scroll_view.scroll_distance = scrol_unit
    scroll_view.scroll_wheel_distance = scrol_unit

    return scroll_view


def get_scrollable_checkboxes_layout(root_checkbox : NodeWidget):
    scroll_layout = BoxLayout(orientation='vertical', size_hint_y=None)
    scroll_layout.bind(minimum_height=scroll_layout.setter('height'))
    recursively_add_boxes(gui_parent=scroll_layout, root_box=root_checkbox, indent=0)

    return scroll_layout


def recursively_add_boxes(gui_parent, root_box : NodeWidget, indent : int):
    if not root_box.get_is_file() and len(root_box.xrd_file_des) == 0:
        return

    root_box.initialize_gui(gui_parent, level=indent)

    for child_box in root_box.active_children:
        recursively_add_boxes(gui_parent=root_box.child_container,
                              root_box=child_box,
                              indent=indent + 1)
