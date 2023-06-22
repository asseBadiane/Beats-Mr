from kivy.uix.boxlayout import BoxLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.button import Button

class TrackStepButton(ToggleButton):
    pass

class TrackSoundButton(Button):
    pass

NB_STEPS_TRACKS = 16
class TrackWidget(BoxLayout):

    def __init__(self, sound, audio_engine, **kwargs):
        super(TrackWidget, self).__init__(**kwargs)

        self.tracks_sound = TrackSoundButton()
        self.tracks_sound.text = sound.displayname
        self.tracks_sound.on_press = self.on_play_sound_button_press
        self.add_widget(self.tracks_sound)

        self.audio_engine = audio_engine
        self.sound = sound

        for i in range(0, NB_STEPS_TRACKS):
            self.add_widget(TrackStepButton())

    def on_play_sound_button_press(self):
        # print("Sound!")
        self.audio_engine.play_sound(self.sound.samples)