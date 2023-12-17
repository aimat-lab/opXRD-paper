from kivy.app import App
from kivy.uix.image import Image
from kivy.animation import Animation
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import PushMatrix, Rotate, PopMatrix
from data_collector.resources import get_loading_icon_path
from kivy.properties import NumericProperty


class LoadingIcon(Image):
    angle = NumericProperty(0)  # Define a custom numeric property for angle

    def __init__(self, **kwargs):
        super(LoadingIcon, self).__init__(**kwargs)
        self.source = 'path/to/your/loading_icon.png'  # Replace with your icon path
        self.anim = Animation(angle=360, duration=2)  # Rotate 360 degrees in 2 seconds
        self.anim += Animation(angle=0, duration=0)  # Reset rotation without delay
        self.anim.repeat = True  # Repeat the animation indefinitely

        # Set up the rotation
        self.bind(angle=self.update_angle)
        self.anim.start(self)

    def update_angle(self, *_):
        self.canvas.before.clear()
        with self.canvas.before:
            PushMatrix()
            Rotate(angle=self.angle, axis=(0, 0, 1), origin=self.center)
        self.canvas.after.clear()
        with self.canvas.after:
            PopMatrix()