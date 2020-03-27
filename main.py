#!/usr/bin/env python
"""A mobile application that helps learn about electricity and magnetism."""

from kivy.app import App
from kivy.uix.button import Button
from kivy.logger import Logger
from kivy.uix.settings import SettingsWithTabbedPanel
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.base import EventLoop

class MenuScreen(Screen):
    """
    Custom Menu Screen.

    It inherits from Screen.
    """
    pass

class MenuScreenButton(Button):
    """
    Custom button style for the Menu Screen.

    It inherits from kivy.uix.button.
    """
    pass

class BackToMenuButton(Button):
    """
    Custom button style to go back to the Menu Screen.

    It inherits from kivy.uix.button.
    """
    pass

class SettingsButton(MenuScreenButton):
    """
    Custom Settings button style for the Menu Screen.

    It inherits from MenuScreenButton, which inherits from kivy.uix.button.
    """
    pass


class StudyScreen(Screen):
    """
    Custom Screen Class for the study section.

    It inherits from Screen.
    """
    pass


class QuizScreen(Screen):
    """
    Custom Screen Class for the Quiz section.

    It inherits from Screen.
    """
    pass

class AboutScreen(Screen):
    """
    Custom Screen Class for the About section.

    It inherits from Screen.
    """
    pass

CONFIG = '''
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





class Gilbert(App):
    """Main class."""

    def build(self):
        """
        Build and return the root widget.
        """
        # The line below is optional. You could leave it out or use one of the
        # standard options, such as SettingsWithSidebar, SettingsWithSpinner
        # etc.
        self.settings_cls = SettingsWithTabbedPanel

        # The ScreenManager controls moving between screens
        self.screen_manager = ScreenManager()

        # Add the screens to the manager and then supply a name
        # that is used to switch screens
        self.screen_manager.add_widget(MenuScreen(name="menu_screen"))
        self.screen_manager.add_widget(StudyScreen(name="study_screen"))
        self.screen_manager.add_widget(QuizScreen(name="quiz_screen"))
        self.screen_manager.add_widget(AboutScreen(name="about_screen"))

        # We apply the saved configuration settings or the defaults
        #root = Builder.load_string(kv)
        #MenuScreenButton = root.ids.MenuScreenButton
        #label.text = self.config.get('My Label', 'text')
        #MenuScreenButton.font_size = float(self.config.get('MenuScreenButton', 'font_size'))
        #return root

        # Bind to catch the "back" Android button.
        self.bind(on_start=self.post_build_init)

        return self.screen_manager

    def post_build_init(self, ev):
        EventLoop.window.bind(on_keyboard=self.hook_keyboard)


    def hook_keyboard(self, window, key, *largs):
        # Key 27 is "Esc" in the Keyboard, or "Back" on Android.
        if key == 27:
            print(self.screen_manager.current)
            if self.screen_manager.current == 'menu_screen':
                print("Can't go further back!")
                Gilbert.get_running_app().stop()
            if isinstance(self.screen_manager.previous, str):
                self.screen_manager.current = self.screen_manager.previous
            else:
                self.screen_manager.current = self.screen_manager.previous()
            return True


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
        settings.add_json_panel('Configuración', self.config, data=CONFIG)

    def on_config_change(self, config, section, key, value):
        """
        Respond to changes in the configuration.
        """
        Logger.info("main.py: App.on_config_change: %s, %s, %s, %s,",
                    config, section, key, value)

        if section == "MenuScreenButton":
            if key == 'font_size':
                #self.MenuScreenButton.font_size = float(value)
                SettingsButton.font_size = float(value)

    def close_settings(self, settings=None):
        """
        The settings panel has been closed.
        """
        Logger.info("main.py: App.close_settings: %s", settings)
        super(Gilbert, self).close_settings(settings)


if __name__ == "__main__":
    Gilbert().run()
