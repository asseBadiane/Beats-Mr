from kivy import Config
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '360')
Config.set('graphics', 'minimum_width', '650')
Config.set('graphics', 'minimum_height', '300')

from kivy.app import App
from kivy.uix.relativelayout import RelativeLayout
from kivy.properties import ObjectProperty, NumericProperty, Clock
from kivy.metrics import dp
from kivy.lang import Builder
from kivy.uix.widget import Widget


from track import TrackWidget
from sound_kit_service import  SoundKitService
from audio_engine import AudioEngine

Builder.load_file("track.kv")
Builder.load_file("play_indicator.kv")

NB_STEPS_TRACKS = 16
MIN_BPM = 80
MAX_BPM = 160

#NB_TRACKS = 4

class VerticalSpacingWidget(Widget):
    pass

class MainWidget(RelativeLayout):
    tracks_layout = ObjectProperty()
    play_indicator_widget = ObjectProperty()
    TRACK_STEP_LEFT_ALIGN = NumericProperty(dp(120))
    step_index = 0
    bpm = NumericProperty(120)
    nb_tracks = NumericProperty(0)


    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)
        self.sound_kit_service = SoundKitService()

        # kik_sound = self.sound_kit_service.get_sound_index(0)

        self.nb_tracks = self.sound_kit_service.get_nb_tracks()
        self.audio_engine = AudioEngine()
        # self.audio_engine.play_sound(kik_sound.samples)

        # self.audio_engine.create_track(kik_sound.samples, 120)
        self.audio_mixer = self.audio_engine.create_mixer(self.sound_kit_service.soundkit.get_all_samples(), self.bpm, NB_STEPS_TRACKS, self.on_mixer_current_step_changed, MIN_BPM)
    

    def on_parent(self, widget, parent):
        self.play_indicator_widget.set_nb_steps(NB_STEPS_TRACKS)
        # self.play_indicator_widget.current_step_index(5)
        for i in range(0, self.sound_kit_service.get_nb_tracks()):
            sound = self.sound_kit_service.get_sound_index(i)
            self.tracks_layout.add_widget(VerticalSpacingWidget())
            self.tracks_layout.add_widget(TrackWidget(sound, self.audio_engine, NB_STEPS_TRACKS, self.audio_mixer.tracks[i], self.TRACK_STEP_LEFT_ALIGN))
        self.tracks_layout.add_widget(VerticalSpacingWidget())

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
        if value <= MIN_BPM:
            self.bpm = MIN_BPM
            return
        if value > MAX_BPM:
            self.bpm = MAX_BPM

        self.audio_mixer.set_bpm(self.bpm)


class MrBeatsApp(App):
    pass


MrBeatsApp().run()