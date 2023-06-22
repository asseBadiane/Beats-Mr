from kivy.app import App
from kivy.uix.relativelayout import RelativeLayout
from kivy.properties import ObjectProperty
from kivy.lang import Builder

from track import TrackWidget
from sound_kit_service import  SoundKitService

Builder.load_file("track.kv")


#NB_TRACKS = 4
class MainWidget(RelativeLayout):
    tracks_layout = ObjectProperty()

    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)

        self.sound_kit_service = SoundKitService()

    def on_parent(self, widget, parent):
        for i in range(0, self.sound_kit_service.get_nb_tracks()):
            sound = self.sound_kit_service.get_sound_index(i)
            self.tracks_layout.add_widget(TrackWidget(sound))


class MrBeatsApp(App):
    pass


MrBeatsApp().run()