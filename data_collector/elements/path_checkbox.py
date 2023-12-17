from __future__ import annotations
from kivy.uix.boxlayout import  BoxLayout

import copy
import os.path
from PIL import Image
from data_collector.elements.selection_widgets import LabeledCheckBox, ImageToggleButton
from data_collector.resources import get_foldericon_path, get_fileicon_path
from data_collector.filesystem import Folder

from typing import Optional
# -------------------------------------------

class PathCheckbox:
    dim = 20
    file_img = Image.open(fp=get_fileicon_path()).resize((dim, dim))
    folder_img = Image.open(fp=get_foldericon_path()).resize((dim, dim))

    def __init__(self,path : str):
        self.path : str = path
        self.active_children: list[PathCheckbox] = self.get_children_from_path()
        self.potential_des : list[PathCheckbox] = []
        self.relevant_des : list[PathCheckbox] =[]
        self.widget : Optional[LabeledCheckBox] = None

        self.child_container = None
        self.total_container = None

    def initialize_gui(self, master_frame, level : int):
        self.total_container = BoxLayout(orientation='vertical', size_hint=(1, None))
        self.total_container.bind(minimum_height=self.total_container.setter('height'))

        # Item container
        item_container = self.make_toggleitem_container(level=level)
        self.total_container.add_widget(item_container)


        # Child container
        if not self.get_is_file():
            self.child_container = self.get_child_container()
            self.total_container.add_widget(self.child_container)

        # Master
        master_frame.add_widget(self.total_container)


    def on_toggle(self, instance, value):
        _ = instance
        if value == 'down':
            self.total_container.remove_widget(self.child_container)
        else:
            self.total_container.add_widget(self.child_container)


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
    # State

    def toggle(self, *args)-> None:
        _ = args
        descendants = self.get_all_relevant_descendants()
        target_value = self.get_value()
        for box in descendants:
            box.set_value(target_value=target_value)

    def set_value(self,target_value : bool):
        self.widget.check_box.active = target_value

    def get_value(self) -> bool:
        return self.widget.check_box.active


    # -------------------------------------------
    # Get filestructure

    def get_is_file(self) -> bool:
        return os.path.isfile(self.path)

    def get_children_from_path(self) -> list[PathCheckbox]:
        if os.path.isfile(self.path):
            children = []
        else:
            this_folder = Folder(path=self.path)
            children = [PathCheckbox(path=path) for path in this_folder.get_children_xrdpaths()]

        return children

    def get_all_relevant_descendants(self) -> list[PathCheckbox]:
        return self.relevant_des

    def get_file_descendants(self):
        return [desecenant for desecenant in self.get_all_relevant_descendants() if desecenant.get_is_file()]

    # -------------------------------------------
    # Get static

    @staticmethod
    def get_child_container():
        child_container = BoxLayout(orientation='vertical', size_hint=(1, None))
        child_container.bind(minimum_height=child_container.setter('height'))
        return child_container


    def make_toggleitem_container(self, level : int):
        toggleitem_container = BoxLayout(orientation='horizontal', size_hint=(1, None))



        self.widget = LabeledCheckBox(text=self._get_text(),
                                      toggle_callback=self.toggle,
                                      height=30,
                                      indent=level,
                                      is_file=self.get_is_file())

        if not self.get_is_file():
            image_btn = ImageToggleButton(size_hint=(None, None),
                                          size=(30,30))

            image_btn.toggle_button.bind(state=self.on_toggle)
            toggleitem_container.add_widget(image_btn)
        else:
            from kivy.uix.label import Label
            place_holder = Label(size_hint=(None,None),size=(30,30))
            toggleitem_container.add_widget(place_holder)



        toggleitem_container.add_widget(self.widget)
        toggleitem_container.bind(minimum_height=toggleitem_container.setter('height'))
        return toggleitem_container


    def _get_text(self) -> str:
        modifier = '' if self.get_is_file() else '/'
        base_name = os.path.basename(os.path.normpath(self.path))

        return f'{modifier}{base_name}'

