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
from kivy.clock import Clock

from typing import Optional
# -------------------------------------------

class PathCheckbox(FsNode):
    dim = get_line_height()
    file_img = Image.open(fp=get_fileicon_path()).resize((dim, dim))
    folder_img = Image.open(fp=get_foldericon_path()).resize((dim, dim))

    def __init__(self,path : str, height : int, scroll_view):
        super().__init__(path=path)
        
        self.height : int = height
        self.potential_des : list[PathCheckbox] = []
        self.relevant_des : list[PathCheckbox] =[]
        self.labeled_checkbox : Optional[LabeledCheckBox] = None
        self.scroll_view = scroll_view
        self.active_children: list[PathCheckbox] = self.get_children_from_path()


        self.child_container = None
        self.total_container = None

    def initialize_gui(self, master_frame, level : int):
        self.total_container = BoxLayout(orientation='vertical', size_hint=(1, None))
        self.total_container.bind(minimum_height=self.total_container.setter('height'))

        # Item container
        self.labeled_checkbox = self._make_label_checkbox(level=level)
        line = self._make_line(labeled_checkbox=self.labeled_checkbox)
        self.total_container.add_widget(line)


        # Child container
        if not self.get_is_file():
            self.child_container = self._get_child_container()
            self.total_container.add_widget(self.child_container)

        # Master
        master_frame.add_widget(self.total_container)




    def recursively_initialize_descendants(self):
        descendants = copy.copy(self.active_children)
        for child in self.active_children:
            child.recursively_initialize_descendants()
            descendants += child.potential_des


        self.potential_des = descendants

        relevant_des = []
        for outer_des in self.potential_des:
            is_relevant = any([des.get_is_file() for des in outer_des.potential_des]) or outer_des.get_is_file()
            relevant_des += [outer_des] if is_relevant else []

        self.relevant_des = relevant_des

    # -------------------------------------------
    # callbacks

    def on_check(self, *args)-> None:
        _ = args
        descendants = self.get_all_relevant_descendants()
        target_value = self.get_value()
        for box in descendants:
            box.set_value(target_value=target_value)


    def set_value(self,target_value : bool):
        self.labeled_checkbox.check_box.active = target_value


    def get_value(self) -> bool:
        return self.labeled_checkbox.check_box.active


    def on_toggle(self, instance, value):
        _ = instance
        h1 = copy.copy(self.scroll_view.children[0].height)
        h2 = copy.copy(self.scroll_view.height)
        s = copy.copy(1-self.scroll_view.scroll_y)

        print(f'h1,h2: {h1},{h2}')

        if value == 'down':
            self.total_container.remove_widget(self.child_container)
        else:
            self.total_container.add_widget(self.child_container)

        Clock.schedule_once(lambda dt: self.calculate_sizes(h1, h2,s))

    def calculate_sizes(self, h1, h2, s):
        h1prime = self.scroll_view.children[0].height
        h2prime = self.scroll_view.height

        target_value = 1 - (h1 - h2) / (h1prime - h2prime) * s
        self.scroll_view.scroll_y = target_value if target_value < 1 else 1

    # -------------------------------------------
    # Get filestructure


    def get_children_from_path(self) -> list[PathCheckbox]:
        if os.path.isfile(self.path):
            children = []
        else:
            this_folder = FsNode(path=self.path)
            children = [PathCheckbox(path=path, height=self.height, scroll_view=self.scroll_view) for path in this_folder.get_children_xrdpaths()]

        return children

    def get_all_relevant_descendants(self) -> list[PathCheckbox]:
        return self.relevant_des

    def get_file_descendants(self):
        return [desecenant for desecenant in self.get_all_relevant_descendants() if desecenant.get_is_file()]



    # -------------------------------------------
    # get

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
