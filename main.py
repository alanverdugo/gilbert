    #!/usr/bin/env python
"""A mobile application that helps learn about electricity and magnetism."""

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
#kivy.require("1.11.1")

class MenuScreenButton(Button):
    """
    Custom button style for the Menu Screen.

    It inherits from kivy.uix.button.
    """

    pass


class Gilbert(App):
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
        button1.bind(on_press=self.say_hello)

        # Create of our custom "Menu-screen buttons".
        button2 = MenuScreenButton(text="Quiz")
        #button2.bind(on_press=self.callback)
        self.add_widget(button2)
        button2.bind(on_press=self.say_hello)

        # Create of our custom "Menu-screen buttons".
        button3 = MenuScreenButton(text="Settings")
        #button3.bind(on_press=self.callback)
        self.add_widget(button3)
        button3.bind(on_press=self.say_hello)


    def say_hello(self, event):
        layout = GridLayout(cols=1, padding=10)

        popup_label = Label(text="Hello")
        close_button = Button(text="Close")

        layout.add_widget(popup_label)
        layout.add_widget(close_button)

        # Instantiate the modal popup and display.
        popup = Popup(title='Message',
                      content=layout,
                      size_hint=(None, None), size=(200, 200))
        popup.open()

        # Attach close button press with popup.dismiss action.
        close_button.bind(on_press=popup.dismiss)


if __name__ == "__main__":
    Gilbert().run()
