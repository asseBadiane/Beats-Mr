from kivy.uix.boxlayout import BoxLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.metrics import dp

class TrackStepButton(ToggleButton):
    pass
     
class TrackSoundButton(Button):
    pass


class TrackWidget(BoxLayout):

    def __init__(self, sound, audio_engine, nb_steps, track_source, steps_left_align, **kwargs):
        super(TrackWidget, self).__init__(**kwargs)

        self.audio_engine = audio_engine
        self.sound = sound
        self.button_steps = []

        self.nb_steps = nb_steps
        self.tracks_source = track_source

        sound_and_separator_layout = BoxLayout()
        sound_and_separator_layout.size_hint_x = None
        sound_and_separator_layout.width = steps_left_align
        self.add_widget(sound_and_separator_layout)

        self.tracks_sound = TrackSoundButton()
        self.tracks_sound.text = sound.displayname
        self.tracks_sound.width = steps_left_align
        self.tracks_sound.on_press = self.on_play_sound_button_press
        sound_and_separator_layout.add_widget(self.tracks_sound)

        # separarteur d'image
        separator_image = Image(source="images/track_separator.png")
        separator_image.size_hint_x = None
        separator_image.width = dp(15)
        sound_and_separator_layout.add_widget(separator_image)
        

        # self.source_tracks = audio_engine.create_track(sound.samples, 120)


        for i in range(0, self.nb_steps):
           
            self.button_step = TrackStepButton()
            if int(i / 4) % 2 == 0:
                self.button_step.background_normal = "images/step_normal1.png"
            else:
                self.button_step.background_normal = "images/step_normal2.png"

            self.button_step.bind(state=self.on_step_button_state)
            self.button_steps.append(self.button_step)
            self.add_widget(self.button_step)

    def on_play_sound_button_press(self):
        # print("Sound!")
        self.audio_engine.play_sound(self.sound.samples)


    def on_step_button_state(self, widget, value):
        
        steps = []
        for i in range(0, self.nb_steps):
            if self.button_steps[i].state == "down":
                steps.append(1)
            else:
                steps.append(0)

       
        self.tracks_source.set_steps( steps)