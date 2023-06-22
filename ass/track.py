
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.togglebutton import ToggleButton

NB_STEPS_TRACK = 16

class TrackStepButton(ToggleButton):
    pass

class TrackWidget(BoxLayout):

    def __init__(self, *args, **kwargs):
        super(TrackWidget, self).__init__(*args, **kwargs)
        for i in range(0, NB_STEPS_TRACK):
            self.add_widget(TrackStepButton())

