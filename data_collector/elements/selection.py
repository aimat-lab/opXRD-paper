from __future__ import annotations

from typing import Optional
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.widget import Widget

from data_collector.resources import get_logo_path
from data_collector.filesystem.fsnode import FsNode
from data_collector.elements.node_widget import NodeWidget
from data_collector.elements.types import ThickVerticalSlider, BlackLabel

from data_collector.configs import get_line_height
import time

# -------------------------------------------

class SelectionLayout(BoxLayout):
    def __init__(self, **kwargs):
        super(SelectionLayout, self).__init__(orientation='horizontal', size_hint=(1, 0.9), **kwargs)
        self.root_checkbox : Optional[NodeWidget] = None

        self.header_layout = self.get_header_widget(num_elements=0)

        self.slider = ThickVerticalSlider(orientation='vertical', min=0, max=1, value=1, size_hint=(0.1, 1))
        self.slider.bind(value=self.adjust_scroll_view)

        self.scroll_view = self.get_scroll_view()
        self.scroll_view.bind(scroll_y=self.on_scroll_view_scroll)

        self.header_layout = self.get_header_widget(num_elements=0)
        self.header_layout.opacity = 0

        self.checkboxes_layout = self.get_checkboxes_layout(file_count_label=self.header_layout,
                                                            scroll_view=self.scroll_view)

        self.add_widget(self.checkboxes_layout)
        self.add_widget(self.slider)


    def set_content(self, path : str):
        self.root_checkbox: NodeWidget = NodeWidget(path=path, height=get_line_height(), scroll_view=self.scroll_view)


        the_time = time.time()
        self.root_checkbox.initialize_fsys()
        print(f'initialization took {time.time() - the_time} seconds')

        new_label = self.get_header_widget(num_elements=len(self.root_checkbox.get_xrd_file_des())).children[2]
        self.header_layout.children[2].text =  new_label.text
        self.header_layout.opacity = 1

        scroll_layout = self.get_scroll_layout(root_checkbox=self.root_checkbox)
        self.scroll_view.add_widget(widget=scroll_layout)


    # -------------------------------------------
    # logic

    def on_scroll_view_scroll(self, instance, value):
        _ = instance
        self.slider.unbind(value=self.adjust_scroll_view)
        self.slider.value = value
        self.slider.bind(value=self.adjust_scroll_view)


    def adjust_scroll_view(self, instance, value):
        _ = instance
        self.scroll_view.scroll_y = value


    # -------------------------------------------
    # elements

    @staticmethod
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

        left_placeholder = Widget(size_hint=(0.4, 1))
        right_placeholder = Widget(size_hint=(0.1, 1))

        layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.125))
        layout.add_widget(left_placeholder)  # Placeholder to balance the layout
        layout.add_widget(file_count_label)
        layout.add_widget(right_placeholder)  # Placeholder to balance the layout
        layout.add_widget(logo_image)

        return layout

    @staticmethod
    def get_checkboxes_layout(file_count_label: Label, scroll_view: ScrollView):
        select_layout = BoxLayout(orientation='vertical')
        select_layout.add_widget(widget=file_count_label)
        select_layout.add_widget(widget=scroll_view)

        return select_layout

    @staticmethod
    def get_scroll_view():
        scroll_view = ScrollView(size_hint=(1, 1), bar_width=0)
        scrol_unit = 200
        scroll_view.scroll_distance = scrol_unit
        scroll_view.scroll_wheel_distance = scrol_unit

        return scroll_view

    def get_scroll_layout(self,root_checkbox: NodeWidget):
        scroll_layout = BoxLayout(orientation='vertical', size_hint_y=None)
        scroll_layout.bind(minimum_height=scroll_layout.setter('height'))
        self.recursively_add_boxes(gui_parent=scroll_layout, root_box=root_checkbox, indent=0)

        return scroll_layout

    def recursively_add_boxes(self,gui_parent, root_box: NodeWidget, indent: int):
        if not root_box.get_is_file() and len(root_box.xrd_node_des) == 0:
            return

        root_box.initialize_gui(gui_parent, level=indent)

        for child_box in root_box.potential_xrd_children:
            self.recursively_add_boxes(gui_parent=root_box.child_container,
                                  root_box=child_box,
                                  indent=indent + 1)
