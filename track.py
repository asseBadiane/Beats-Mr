from kivy.uix.boxlayout import BoxLayout
from kivy.uix.togglebutton import ToggleButton


class TrackStepButton(ToggleButton):
    pass


NB_STEPS_TRACKS = 16
class TrackWidget(BoxLayout):

    def __init__(self, **kwargs):
        super(TrackWidget, self).__init__(**kwargs)
        for i in range(0, NB_STEPS_TRACKS):
            self.add_widget(TrackStepButton())