    #!/usr/bin/env python
"""A mobile application that helps learn about electricity and magnetism."""

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.logger import Logger
from kivy.lang import Builder
from kivy.uix.settings import SettingsWithSidebar
#kivy.require("1.11.1")

class MenuScreenButton(Button):
    """
    Custom button style for the Menu Screen.

    It inherits from kivy.uix.button.
    """
    pass

class SettingsButton(MenuScreenButton):
    """
    Custom Settings button style for the Menu Screen.

    It inherits from MenuScreenButton, which inherits from kivy.uix.button.
    """
    pass


config = '''
[
    {
        "type": "numeric",
        "title": "MenuScreenButton font size",
        "desc": "Choose the font size the MenuScreenButton",
        "section": "MenuScreenButton",
        "key": "font_size"
    }
]
'''

Logger.critical(SettingsButton.font_size)

class Gilbert(App):
    """Main class."""

    def build(self):
        """
        Build and return the root widget.
        """
        # The line below is optional. You could leave it out or use one of the
        # standard options, such as SettingsWithSidebar, SettingsWithSpinner
        # etc.
        self.settings_cls = SettingsWithSidebar

        # We apply the saved configuration settings or the defaults
        #root = Builder.load_string(kv)
        #MenuScreenButton = root.ids.MenuScreenButton
        #label.text = self.config.get('My Label', 'text')
        #MenuScreenButton.font_size = float(self.config.get('MenuScreenButton', 'font_size'))
        #return root
        return MenuScreen()

    def build_config(self, config):
        """
        Set the default values for the configs sections.
        """
        config.setdefaults('MenuScreenButton', {'font_size': 20})

    def build_settings(self, settings):
        """
        Add our custom section to the default configuration object.
        """
        # We use the string defined above for our config JSON, but it could also be
        # loaded from a file as follows:
        #     settings.add_json_panel('My Label', self.config, 'settings.json')
        settings.add_json_panel('Configuraciones varias', self.config, data=config)

    def on_config_change(self, config, section, key, value):
        """
        Respond to changes in the configuration.
        """
        Logger.info("main.py: App.on_config_change: {0}, {1}, {2}, {3}".format(
            config, section, key, value))

        if section == "MenuScreenButton":
            if key == 'font_size':
                #self.MenuScreenButton.font_size = float(value)
                SettingsButton.font_size = float(value)

    def close_settings(self, settings=None):
        """
        The settings panel has been closed.
        """
        Logger.info("main.py: App.close_settings: {0}".format(settings))
        super(Gilbert, self).close_settings(settings)


class MenuScreen(BoxLayout):
    """Main menu screen."""

    def __init__(self, **kwargs):
        super(MenuScreen, self).__init__(**kwargs)

        # Create one of our custom "Menu-screen buttons".
        button1 = MenuScreenButton(text="Study")
        #button1.bind(on_press=self.callback)
        self.add_widget(button1)
        button1.bind(on_press=self.say_hello)

        # Create one of our custom "Menu-screen buttons".
        button2 = MenuScreenButton(text="Quiz")
        #button2.bind(on_press=self.callback)
        self.add_widget(button2)
        button2.bind(on_press=self.say_hello)

        # Create our custom "Settings button".
        button3 = SettingsButton()
        #button3.bind(on_press=self.callback)
        self.add_widget(button3)
        #button3.bind(on_press=app.open_settings())


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
