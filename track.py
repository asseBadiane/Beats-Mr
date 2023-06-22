from kivy.uix.boxlayout import BoxLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.button import Button

class TrackStepButton(ToggleButton):
    pass

class TrackSoundButton(Button):
    pass

NB_STEPS_TRACKS = 16
class TrackWidget(BoxLayout):

    def __init__(self, sound, **kwargs):
        super(TrackWidget, self).__init__(**kwargs)

        self.tracks_sound = TrackSoundButton()
        self.tracks_sound.text = sound.displayname
        self.add_widget(self.tracks_sound)

        for i in range(0, NB_STEPS_TRACKS):
            self.add_widget(TrackStepButton())
