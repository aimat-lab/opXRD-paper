from __future__ import annotations

from data_collector.elements.types import LabeledCheckBox
from abc import abstractmethod

from typing import Optional
# -------------------------------------------

class DynamicElem:

    def __init__(self, height : int):
        super().__init__()

        self.labeled_checkbox : Optional[LabeledCheckBox] = None

        self.child_container = None
        self.total_container = None
        self.height = height
        self.child_nodes : list[DynamicElem] = []
        self.parent : Optional[DynamicElem] = None

    # -------------------------------------------
    # callbacks

    @abstractmethod
    def unload(self):
        pass


    @abstractmethod
    def load(self):
        pass

    # -------------------------------------------
    # get

    @staticmethod
    def get_visibile_subnodes_in_range(node : DynamicElem, start_y : int, end_y : int) -> list:
        selected_nodes = []

        def dfs(current_node):
            ypos = current_node.get_ypos()
            if start_y <= ypos <= end_y:
                selected_nodes.append(current_node)

            if ypos <= end_y:
                for child in current_node.get_gui_child_nodes():
                    dfs(child)

        dfs(node)
        return selected_nodes


    def get_ypos(self) -> int:
        if self.parent is None:
            return 0

        parent_gui_children = self.parent.get_gui_child_nodes()
        child_index = parent_gui_children.index(self)
        previous_children = parent_gui_children[:child_index]

        ypos = self.parent.get_ypos() + sum([child.total_container.height for child in previous_children]) + self.parent.height
        return ypos

    def get_gui_child_nodes(self):
        return [child for child in self.child_nodes if child.total_container]

