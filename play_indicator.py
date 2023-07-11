from kivy.uix.boxlayout import BoxLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.button import Button
from kivy.properties import NumericProperty
from kivy.uix.image import Image
from kivy.uix.widget import Widget


# class PlayIndicatorButton(ToggleButton):
#     pass
class PlayIndicatorLight(Image):
    pass


class PlayIndicatorWidget(BoxLayout):
    nb_steps = 0
    buttons = []
    left_align = NumericProperty(0)


    def set_nb_steps(self, nb_steps):

        if not nb_steps == self.nb_steps:
            self.lights = []
            self.clear_widgets()

            dummy_widget = Widget()
            dummy_widget.size_hint_x = None
            dummy_widget.width = self.left_align
            dummy_widget.disabled = True
            self.add_widget(dummy_widget)

            for i in range(0, nb_steps):
                light = PlayIndicatorLight()
                light.source = "images/indicator_light_off.png"

                self.lights.append(light)
                self.add_widget(light)

            self.nb_steps = nb_steps


    def current_step_index(self, index):
        if index >= len(self.lights):
            return
        for i in range(0, len(self.lights)):
            light = self.lights[i]
            if i == index:
                
                light.source = "images/indicator_light_on.png"
               
            else:
                light.source = "images/indicator_light_off.png"