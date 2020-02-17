#!/usr/bin/env python
"""A mobile application that helps learn about electricity and magnetism."""

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
#kivy.require("1.11.1")

class MenuScreenButton(Button):
    """
    Custom button style for the Menu Screen.

    It inherits from kivy.uix.button.
    """

    pass


class Magnes(App):
    """Main class."""

    def build(self):
        """Initialize."""
        return MenuScreen()


class MenuScreen(BoxLayout):
    """Main menu screen."""

    def __init__(self, **kwargs):
        super(MenuScreen, self).__init__(**kwargs)

        # Create of our custom "Menu-screen buttons".
        button1 = MenuScreenButton(text="Study")
        #button1.bind(on_press=self.callback)
        self.add_widget(button1)

        # Create of our custom "Menu-screen buttons".
        button2 = MenuScreenButton(text="Quiz")
        #button2.bind(on_press=self.callback)
        self.add_widget(button2)

        # Create of our custom "Menu-screen buttons".
        button3 = MenuScreenButton(text="Settings")
        #button3.bind(on_press=self.callback)
        self.add_widget(button3)


if __name__ == "__main__":
    Magnes().run()
