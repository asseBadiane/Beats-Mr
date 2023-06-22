from kivy.app import App
from kivy.uix.relativelayout import RelativeLayout


from kivy.lang import Builder

Builder.load_file("track.kv")



class MainWidget(RelativeLayout):
    pass




class MrBeatsApp(App):
    pass


MrBeatsApp().run()