from kivy.app import App
from kivy.uix.relativelayout import RelativeLayout
from kivy.properties import ObjectProperty


from track import TrackWidget
from kivy.lang import Builder

Builder.load_file("track.kv")


NB_TRACKS = 4
class MainWidget(RelativeLayout):
    tracks_layout = ObjectProperty()


    def on_parent(self, widget, parent):
        for i in range(0, NB_TRACKS):
            self.tracks_layout.add_widget(TrackWidget())


class MrBeatsApp(App):
    pass


MrBeatsApp().run()