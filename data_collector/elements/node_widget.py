from __future__ import annotations
from kivy.uix.boxlayout import  BoxLayout

import copy
import os.path
from PIL import Image
from data_collector.elements.types import LabeledCheckBox, IconToggleButton
from data_collector.resources import get_foldericon_path, get_fileicon_path
from data_collector.filesystem import FsNode
from data_collector.configs import get_line_height
from kivy.uix.label import Label
# from kivy.clock import Clock

from typing import Optional
# -------------------------------------------

class NodeWidget(FsNode):
    dim = get_line_height()
    file_img = Image.open(fp=get_fileicon_path()).resize((dim, dim))
    folder_img = Image.open(fp=get_foldericon_path()).resize((dim, dim))

    def __init__(self,path : str, height : int, scroll_view):
        super().__init__(path=path)

        self.height : int = height
        self.labeled_checkbox : Optional[LabeledCheckBox] = None
        self.scroll_view = scroll_view

        self.child_container = None
        self.total_container = None
        self.line = None
        self.child_nodes : list[NodeWidget] = []
        self.parent : Optional[NodeWidget] = None
        self.place_holder = None


    def initialize_gui(self, gui_parent, level : int):
        self.total_container = BoxLayout(orientation='vertical', size_hint=(1, None))
        self.total_container.bind(minimum_height=self.total_container.setter('height'))

        self.labeled_checkbox = self._make_label_checkbox(level=level)
        self.line = self._make_line(labeled_checkbox=self.labeled_checkbox)
        self.total_container.add_widget(self.line)
        self.place_holder = self.get_placeholder()

        if not self.get_is_file():
            self.child_container = self._get_child_container()
            self.total_container.add_widget(self.child_container)

        gui_parent.add_widget(self.total_container)


    def make_child(self, name : str):
        path = os.path.join(self.path,name)
        child = NodeWidget(path=path, height=self.height, scroll_view=self.scroll_view)
        child.parent = self
        self.child_nodes += [child]
        return child

    # -------------------------------------------
    # callbacks

    def on_check(self, *args)-> None:
        _ = args
        descendants = self.xrd_node_des
        target_value = self.get_is_checked()
        for box in descendants:
            box.set_value(target_value=target_value)


    def set_value(self,target_value : bool):
        self.labeled_checkbox.check_box.active = target_value


    def get_is_checked(self) -> bool:
        return self.labeled_checkbox.check_box.active


    def on_toggle(self, instance, value):
        _ = instance
        scroll_height = copy.copy(self.scroll_view.children[0].height)
        vp_height = copy.copy(self.scroll_view.height)
        s = copy.copy(1-self.scroll_view.scroll_y)

        factor = -1 if value == 'down' else 1
        height_delta =  factor * self.child_container.height

        with self.scroll_view.canvas:
            if value == 'down':
                self.total_container.remove_widget(self.child_container)
            else:
                self.total_container.add_widget(self.child_container)

            self.adjust_scroll(scroll_height=scroll_height, vp_height=vp_height,
                               new_scroll_height=scroll_height + height_delta, s=s)


    def adjust_scroll(self, scroll_height, vp_height,  new_scroll_height, s):
        viewport_height = self.scroll_view.height

        target_value = 1 - (scroll_height - vp_height) / (new_scroll_height - viewport_height) * s
        self.scroll_view.scroll_y = target_value if target_value < 1 else 1


    def unload(self):
        self.total_container.remove_widget(self.line)
        self.total_container.add_widget(self.place_holder ,index=0)
    

    def load(self):
        self.total_container.remove_widget(self.place_holder)
        self.total_container.add_widget(self.line,index=0)

    # -------------------------------------------
    # get

    def get_ypos(self) -> int:
        if self.parent is None:
            return 0

        parent_gui_children = self.parent.get_gui_child_nodes()
        child_index = parent_gui_children.index(self)
        previous_children = parent_gui_children[:child_index+1]

        ypos = self.parent.get_ypos() + sum([child.total_container.height for child in previous_children])
        return ypos

    def get_gui_child_nodes(self):
        return [child for child in self.child_nodes if child.total_container]


    def _make_label_checkbox(self, level : int):
        labeled_checkbox = LabeledCheckBox(text=self._get_text(),
                                            check_callback=self.on_check,
                                            indent=level,
                                            is_file=self.get_is_file(),
                                            height=self.height)
        return labeled_checkbox


    def _get_text(self) -> str:
        modifier = '' if self.get_is_file() else '/'
        base_name = os.path.basename(os.path.normpath(self.path))

        return f'{modifier}{base_name}'


    def _make_line(self, labeled_checkbox : LabeledCheckBox):
        line_container = BoxLayout(orientation='horizontal', size_hint=(1, None))

        if not self.get_is_file():
            icon_toggle_button = IconToggleButton(size_hint=(None, None),
                                          size=(self.height,self.height))

            icon_toggle_button.btn.bind(state=self.on_toggle)
            line_container.add_widget(icon_toggle_button)
        else:
            place_holder = Label(size_hint=(None,None),size=(self.height,self.height))
            line_container.add_widget(place_holder)

        line_container.add_widget(labeled_checkbox)
        line_container.bind(minimum_height=line_container.setter('height'))
        return line_container


    @staticmethod
    def _get_child_container():
        child_container = BoxLayout(orientation='vertical', size_hint=(1, None))
        child_container.bind(minimum_height=child_container.setter('height'))
        return child_container


    def get_placeholder(self):
        line_container = BoxLayout(orientation='horizontal', size_hint=(1, None))
        place_holder = Label(size_hint=(None, None), size=(self.height, self.height))
        line_container.add_widget(place_holder)
        line_container.bind(minimum_height=line_container.setter('height'))
        return line_container