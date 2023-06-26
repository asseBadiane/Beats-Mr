from kivy.uix.boxlayout import BoxLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.button import Button
from kivy.properties import NumericProperty


class PlayIndicatorButton(ToggleButton):
    pass


class PlayIndicatorWidget(BoxLayout):
    nb_steps = 0
    buttons = []
    left_align = NumericProperty(0)


    def set_nb_steps(self, nb_steps):

        if not nb_steps == self.nb_steps:
            self.buttons = []
            self.clear_widgets()

            dummy_button = Button()
            dummy_button.size_hint_x = None
            dummy_button.width = self.left_align
            self.add_widget(dummy_button)

            for i in range(0, nb_steps):
                button = PlayIndicatorButton()
                self.buttons.append(button)
                self.add_widget(button)

            self.nb_steps = nb_steps

