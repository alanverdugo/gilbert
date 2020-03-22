#!/usr/bin/env python
"""A mobile application that helps learn about electricity and magnetism."""

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
#from kivy.uix.boxlayout import BoxLayout
#from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.logger import Logger
#from kivy.lang import Builder
from kivy.uix.settings import SettingsWithTabbedPanel
from kivy.uix.screenmanager import ScreenManager, Screen

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

        # We apply the saved configuration settings or the defaults
        #root = Builder.load_string(kv)
        #MenuScreenButton = root.ids.MenuScreenButton
        #label.text = self.config.get('My Label', 'text')
        #MenuScreenButton.font_size = float(self.config.get('MenuScreenButton', 'font_size'))
        #return root
        return self.screen_manager

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

"""
class MenuScreen(BoxLayout):
    ""Main menu screen.""

    def __init__(self, **kwargs):
        #super(MenuScreen, self).__init__(**kwargs)

        # Create one of our custom "Menu-screen buttons".
        button1 = MenuScreenButton(text="Study")
        #button1.bind(on_press=self.callback)
        self.add_widget(button1)
        button1.bind(on_press=self.open_study_section)

        # Create one of our custom "Menu-screen buttons".
        button2 = MenuScreenButton(text="Quiz")
        #button2.bind(on_press=self.callback)
        self.add_widget(button2)
        button2.bind(on_press=open_quiz_section)

        # Create our custom "Settings button".
        button3 = SettingsButton()
        self.add_widget(button3)

    def open_study_section(self, event):
        #StudyScreen.manager.transition.direction = 'left'
        #StudyScreen.manager.transition.duration = 1
        #StudyScreen.manager.current = 'MenuScreen'
        print(self.screen_manager.next())
        self.screen_manager.transition.direction = 'left'
        self.screen_manager.transition.duration = 1
        self.screen_manager.current = self.screen_manager.next()
        #self.screen_manager.current = "study_screen"
"""

def open_quiz_section(event):
    layout = GridLayout(cols=1, padding=10)

    popup_label = Label(text="Quiz section")
    close_button = Button(text="Close")

    layout.add_widget(popup_label)
    layout.add_widget(close_button)

    # Instantiate the modal popup and display.
    popup = Popup(title='Redirecting to...',
                  content=layout,
                  size_hint=(None, None),
                  size=(400, 400))
    popup.open()

    # Attach close button press with popup.dismiss action.
    close_button.bind(on_press=popup.dismiss)


if __name__ == "__main__":
    Gilbert().run()
