from kivy.uix.boxlayout import BoxLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.button import Button

class TrackStepButton(ToggleButton):
    pass

class TrackSoundButton(Button):
    pass


class TrackWidget(BoxLayout):

    def __init__(self, sound, audio_engine, nb_steps_track, **kwargs):
        super(TrackWidget, self).__init__(**kwargs)

        self.tracks_sound = TrackSoundButton()
        self.tracks_sound.text = sound.displayname
        self.tracks_sound.on_press = self.on_play_sound_button_press
        self.add_widget(self.tracks_sound)

        self.audio_engine = audio_engine
        self.sound = sound
        self.button_steps = []

        self.nb_steps_track = nb_steps_track

        # self.source_tracks = audio_engine.create_track(sound.samples, 120)

        for i in range(0, self.nb_steps_track):
            self.button_step = TrackStepButton()
            self.button_step.bind(state=self.on_step_button_state)
            self.button_steps.append(self.button_step)
            self.add_widget(self.button_step)

    def on_play_sound_button_press(self):
        # print("Sound!")
        self.audio_engine.play_sound(self.sound.samples)


    def on_step_button_state(self, widget, value):
        
        steps = []
        for i in range(0, self.nb_steps_track):
            if self.button_steps[i].state == "down":
                steps.append(1)
            else:
                steps.append(0)

        # self.source_tracks.set_steps(steps)