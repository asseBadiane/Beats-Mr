from kivy.app import App
from kivy.uix.relativelayout import RelativeLayout
from kivy.properties import ObjectProperty
from kivy.lang import Builder

from track import TrackWidget
from sound_kit_service import  SoundKitService
from audio_engine import AudioEngine

Builder.load_file("track.kv")
NB_STEPS_TRACKS = 16

#NB_TRACKS = 4
class MainWidget(RelativeLayout):
    tracks_layout = ObjectProperty()

    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)
        self.sound_kit_service = SoundKitService()

        # kik_sound = self.sound_kit_service.get_sound_index(0)

        self.audio_engine = AudioEngine()
        # self.audio_engine.play_sound(kik_sound.samples)

        # self.audio_engine.create_track(kik_sound.samples, 120)
        self.audio_mixer = self.audio_engine.create_mixer(self.sound_kit_service.soundkit.get_all_samples(), 120, NB_STEPS_TRACKS)


    def on_parent(self, widget, parent):
        for i in range(0, self.sound_kit_service.get_nb_tracks()):
            sound = self.sound_kit_service.get_sound_index(i)
            self.tracks_layout.add_widget(TrackWidget(sound, self.audio_engine, NB_STEPS_TRACKS, self.audio_mixer.tracks[i]))
        

class MrBeatsApp(App):
    pass


MrBeatsApp().run()