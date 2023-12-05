from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
# from kivy.core.window import Window
from kivy.uix.label import Label
# from kivy.uix.slider import Slider
from data_collector.elements.path_checkbox import PathCheckbox

# -------------------------------------------

def get_select_layout(file_count_label: Label, scroll_view: ScrollView):
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
    if not root_box.get_is_file() and len(root_box.get_file_descendants()) == 0:
        return

    root_box.initialize_gui(gui_parent, level=indent)

    for child_box in root_box.active_children:
        recursively_add_boxes(gui_parent=root_box.child_container,
                              root_box=child_box,
                              indent=indent + 1)


