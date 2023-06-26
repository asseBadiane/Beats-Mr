from kivy.app import App
from kivy.uix.relativelayout import RelativeLayout
from kivy.properties import ObjectProperty, NumericProperty, Clock
from kivy.metrics import dp
from kivy.lang import Builder


from track import TrackWidget
from sound_kit_service import  SoundKitService
from audio_engine import AudioEngine

Builder.load_file("track.kv")
Builder.load_file("play_indicator.kv")

NB_STEPS_TRACKS = 16

#NB_TRACKS = 4
class MainWidget(RelativeLayout):
    tracks_layout = ObjectProperty()
    play_indicator_widget = ObjectProperty()
    TRACK_STEP_LEFT_ALIGN = NumericProperty(dp(100))
    step_index = 0
    bpm = NumericProperty(120)


    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)
        self.sound_kit_service = SoundKitService()

        # kik_sound = self.sound_kit_service.get_sound_index(0)

        self.audio_engine = AudioEngine()
        # self.audio_engine.play_sound(kik_sound.samples)

        # self.audio_engine.create_track(kik_sound.samples, 120)
        self.audio_mixer = self.audio_engine.create_mixer(self.sound_kit_service.soundkit.get_all_samples(), 120, NB_STEPS_TRACKS, self.on_mixer_current_step_changed)
    

    def on_parent(self, widget, parent):
        self.play_indicator_widget.set_nb_steps(NB_STEPS_TRACKS)
        # self.play_indicator_widget.current_step_index(5)
        for i in range(0, self.sound_kit_service.get_nb_tracks()):
            sound = self.sound_kit_service.get_sound_index(i)
            self.tracks_layout.add_widget(TrackWidget(sound, self.audio_engine, NB_STEPS_TRACKS, self.audio_mixer.tracks[i], self.TRACK_STEP_LEFT_ALIGN))
        

    def on_mixer_current_step_changed(self, step_index):
        # print(f"on_mixer_current_step_changed {step_index}")
        self.step_index = step_index
        
        Clock.schedule_once(self.update_play_indicator_cbk, 0)

    def update_play_indicator_cbk(self, dt):
        if self.play_indicator_widget is not None:
            self.play_indicator_widget.current_step_index(self.step_index)

    def on_play_button_pressed(self):
        self.audio_mixer.audio_play()

    def on_stop_button_pressed(self):
        self.audio_mixer.audio_stop()
     

    def on_bpm(self, widget, value):
        if value <= 80:
            self.bpm = 80
            return
        if value > 160:
            self.bpm = 160


class MrBeatsApp(App):
    pass


MrBeatsApp().run()