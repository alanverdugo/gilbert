#!/usr/bin/env python
"""A mobile application that helps learn about electricity and magnetism."""

# Operating System functionality.
import os

# Shuffle answers in quizzes to confuse students.
import random

# SQLite connections and retrieval.
import sqlite3

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.slider import Slider
from kivy.uix.dropdown import DropDown
from kivy.uix.settings import SettingsWithTabbedPanel
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.rst import RstDocument
from kivy.uix.popup import Popup

# Layouts
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout

from kivy.logger import Logger
from kivy.base import EventLoop

import kivy
kivy.require('1.11.1')


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

class PurpleRoundedButton(Button):
    """
    Custom button style for the "back to menu" and "reset" buttons.

    It inherits from kivy.uix.button.
    """
    pass

class QuestionLabel(Label):
    """
    Custom Label that wraps its text in case it is too long.

    It inherits from from kivy.uix.label
    """

class BackToMenuButton(PurpleRoundedButton):
    """
    Custom button style to go back to the Menu Screen.

    It inherits from kivy.uix.button.
    """
    pass

class ResetOhmButton(PurpleRoundedButton):
    """
    Custom button reset the Ohm simulator.

    It inherits from kivy.uix.button.
    """
    def on_press(self):
        """
        Set the Sliders values to their defaults.
        """
        # Reset to the default image.
        self.parent.parent.triangle_image.source = "assets/images/I_318px-law_triangle.png"
        self.parent.parent.selected = "current"
        # Reset sliders' status.
        self.parent.parent.current_slider.disabled = True
        self.parent.parent.voltage_slider.disabled = False
        self.parent.parent.resistance_slider.disabled = False
        # Reset sliders' values.
        self.parent.parent.current_slider.value = 0.2
        self.parent.parent.current_slider.min = 0.1
        self.parent.parent.current_slider.max = 900

        self.parent.parent.voltage_slider.value = 0.1
        self.parent.parent.voltage_slider.min = 0.1
        self.parent.parent.voltage_slider.max = 9

        self.parent.parent.resistance_slider.value = 500
        self.parent.parent.resistance_slider.min = 10
        self.parent.parent.resistance_slider.max = 1000

class SettingsButton(MenuScreenButton):
    """
    Custom Settings button style for the Menu Screen.

    It inherits from MenuScreenButton, which inherits from kivy.uix.button.
    """
    pass

class AboutButton(MenuScreenButton):
    """
    Custom "About" button style for the Menu Screen.

    It inherits from MenuScreenButton, which inherits from kivy.uix.button.
    """
    pass

class StudyScreen(Screen):
    """
    Custom Screen Class for the study section.

    It inherits from Screen.
    """
    def __init__(self, **kwargs):
        super(StudyScreen, self).__init__(**kwargs)

        # Create a float layout.
        self.float_layout = FloatLayout()
        self.add_widget(self.float_layout)

        # Add the right side of the screen, where we will show the text.
        self.rst_document = RstDocument(source="assets/chapters/chapter01.rst",
                                        show_errors=True,
                                        size_hint=(0.8, 1),
                                        pos_hint={"right":1, "top":1})
        self.float_layout.add_widget(self.rst_document)

        # Add the dropdown "menu" at the left of the screen.
        self.dropdown = DropDown()
        for chapter in ['01', '02', '03', '04']:
            # when adding widgets, we need to specify the height manually (disabling
            # the size_hint_y) so the dropdown can calculate the area it needs.
            btn = Button(text='%r' % chapter,
                         height=100,
                         size_hint_y=None)

            # For each button, attach a callback that will call the select() method
            # on the dropdown. We'll pass the text of the button as the data of the
            # selection.
            btn.bind(on_release=lambda btn: self.dropdown.select(btn.text))
            # Add another bind so the RST document is updated according to the selection.
            btn.bind(on_press=lambda btn: self.update_study_text(btn.text))

            # Add the button inside the dropdown.
            self.dropdown.add_widget(btn)

        # Create a big main button to open the dropdown.
        self.mainbutton = Button(text='Lecciones',
                                 size_hint=(0.2, 0.2),
                                 pos_hint={"left":0, "top":1})

        # Show the dropdown menu when the main button is released
        # note: all the bind() calls pass the instance of the caller (here, the
        # mainbutton instance) as the first argument of the callback (here,
        # dropdown.open).
        self.mainbutton.bind(on_release=self.dropdown.open)

        # Listen for the selection in the dropdown list and
        # assign the data to the button text.
        self.dropdown.bind(on_select=lambda instance, x: setattr(self.mainbutton, 'text', x))

        self.float_layout.add_widget(self.mainbutton)

        # Outside the grid layout (but inside the float layout), add the back button.
        self.back_to_menu_button = BackToMenuButton(pos_hint={"left":0, "bottom":1},
                                                    size_hint=(0.2, 0.1))
        self.float_layout.add_widget(self.back_to_menu_button)


    def update_study_text(self, chapter):
        """
        Update the text in the RST widget according to the dropdown selection.
        """
        self.rst_document.source = "assets/chapters/chapter" + chapter.replace("'", "") + ".rst"


class QuizScreen(Screen):
    """
    Custom Screen Class for the Quiz section.

    It inherits from Screen.
    """
    def __init__(self, **kwargs):
        super(QuizScreen, self).__init__(**kwargs)

        # Place holders for questions' data.
        self.question_id = ""
        self.question_text = ""
        self.correct_answer = ""

        # Create a float layout.
        self.float_layout = FloatLayout()
        self.add_widget(self.float_layout)

        # Title label
        title_label = Label(text="QuizScreen",
                            size_hint=(0.5, 0.05),
                            pos_hint={"center_x": 0.5, "top": 1})
        self.float_layout.add_widget(title_label)

        # Question label
        self.question_label = QuestionLabel(halign="center",
                                            valign="middle",
                                            pos_hint={"center_x": 0.5, "top": 0.9})
        self.float_layout.add_widget(self.question_label)

        # Back to menu button.
        self.back_to_menu_button = BackToMenuButton(pos_hint={"left":0, "bottom":1},
                                                    size_hint=(0.2, 0.1))
        self.float_layout.add_widget(self.back_to_menu_button)

        # Create a box layout inside the float layout (to contain the answer buttons).
        self.answers_box_layout = BoxLayout(orientation="vertical",
                                            spacing=20,
                                            pos_hint={"center_x":0.5, "top":0.7},
                                            size_hint=(0.5, 0.6))
        self.float_layout.add_widget(self.answers_box_layout)

        # Outside the grid layout (but inside the float layout), add the reset button.
        reset_quiz_button = ResetOhmButton(pos_hint={"right":1, "bottom":1},
                                           size_hint=(0.2, 0.1))
        self.float_layout.add_widget(reset_quiz_button)

        # Connect to the SQLite DB and create a cursor.
        project_dir = os.path.dirname(os.path.realpath(__file__))
        connection = sqlite3.connect(os.path.join(os.sep, project_dir,
                                                  "db", "questions.db"))
        self.cursor = connection.cursor()

        # Get a random question from the DB and display it.
        self.get_random_question()


    def get_random_question(self):
        """
        Retrieve data from the SQLite DB.
        """

        # Get a random question.
        self.cursor.execute("SELECT * FROM questions ORDER BY RANDOM() LIMIT 1")
        # Fetch all returns a list with a tuple.
        question = self.cursor.fetchall()

        # Show the question text into the question label.
        self.question_label.text = str(question[0][1])

        # Get answers to this question.
        self.get_answers()

    def get_answers(self):
        """
        Get the corresponding answers for the current question.
        """
        # Execute the query to get the answers to the current question.
        self.cursor.execute("SELECT * FROM answers "
                            "INNER JOIN questions "
                            "ON questions.question_id = answers.question_id "
                            f"WHERE questions.question_text = '{self.question_label.text}'")
        # Fetch all returns a list with a tuple.
        answers = self.cursor.fetchall()

        # Get the correct answer.
        self.cursor.execute("SELECT answer_text FROM answers "
                            "INNER JOIN questions "
                            "ON questions.question_id = answers.question_id "
                            f"WHERE questions.question_text = '{self.question_label.text}'"
                            "AND answers.is_correct = 1")
        self.correct_answer = self.cursor.fetchall()[0][0]

        # Format that into a list.
        answers_list = [answer[1] for answer in answers]
        # Shuffle the answers to make the quiz harder.
        random.shuffle(answers_list)

        # Create the answer buttons.
        for answer in answers_list:
            answer_button = PurpleRoundedButton(text=answer)

            # For each button, attach a callback that will call the check_answer method
            # We'll pass the text of the button as the data of the selection.
            answer_button.bind(on_release=lambda answer_button: self.check_answer(answer_button.text))

            # Add the button inside the box layout for the answers.
            self.answers_box_layout.add_widget(answer_button)

    def check_answer(self, selected_answer):
        """
        Check if the selected answer is correct or not.
        """
        if selected_answer == self.correct_answer:
            popup = Popup(title='Congratulations!',
                          content=Label(text='Correct!'),
                          size_hint=(0.3, 0.3))
        else:
            popup = Popup(title='Try again!',
                          content=Label(text='Wrong!'),
                          size_hint=(0.3, 0.3))
        popup.open()


class OhmScreen(Screen):
    """
    Custom Screen Class for the Ohm's law simulator section.

    It inherits from Screen.
    """
    def __init__(self, **kwargs):
        super(OhmScreen, self).__init__(**kwargs)

        # Default value to be calculated.
        self.selected = "current"

        # Create a float layout.
        self.float_layout = FloatLayout()
        self.add_widget(self.float_layout)

        # Title label
        title_label = Label(text="Simulador de la ley de Ohm",
                            size_hint=(0.5, 0.05),
                            pos_hint={"center_x": 0.5, "top": 1})
        self.float_layout.add_widget(title_label)

        # Triangle image.
        self.triangle_image = Image(source="assets/images/I_318px-law_triangle.png",
                                    keep_ratio=False,
                                    #size_hint=(0.3, 0.3),
                                    size_hint=(None, None),
                                    width=400,
                                    height=400,
                                    allow_stretch=True,
                                    pos_hint={"center_x": 0.5, "top": 0.97})
        self.float_layout.add_widget(self.triangle_image)

        # Invisible grid layout and buttons for the triangle image.
        triangle_grid_layout = GridLayout(rows=2, cols=2,
                                          pos_hint={'center_x':0.5, "top": 0.97},
                                          size=(400, 400),
                                          size_hint=(None, None))
        triangle_top_left_button = Button(id="triangle_top_left_button",
                                          size_hint_x=None, width=200,
                                          size_hint_y=None, height=200,
                                          opacity=0)
        triangle_top_left_button.bind(on_press=self.deactivate_sliders)
        triangle_grid_layout.add_widget(triangle_top_left_button)

        triangle_top_right_button = Button(id="triangle_top_right_button",
                                           size_hint_x=None, width=200,
                                           size_hint_y=None, height=200,
                                           background_color=(0, 0, 0, 0),
                                           background_normal="")
        triangle_top_right_button.bind(on_press=self.deactivate_sliders)
        triangle_grid_layout.add_widget(triangle_top_right_button)

        triangle_bottom_left_button = Button(id="triangle_bottom_left_button",
                                             size_hint_x=None, width=200,
                                             size_hint_y=None, height=200,
                                             background_color=(0, 0, 0, 0),
                                             background_normal="")
        triangle_bottom_left_button.bind(on_press=self.deactivate_sliders)
        triangle_grid_layout.add_widget(triangle_bottom_left_button)

        triangle_bottom_right_button = Button(id="triangle_bottom_right_button",
                                              size_hint_x=None, width=200,
                                              size_hint_y=None, height=200,
                                              background_color=(0, 0, 0, 0),
                                              background_normal="")
        triangle_bottom_right_button.bind(on_press=self.deactivate_sliders)
        triangle_grid_layout.add_widget(triangle_bottom_right_button)

        self.float_layout.add_widget(triangle_grid_layout)

        # Back to menu button.
        self.back_to_menu_button = BackToMenuButton(pos_hint={"left":0, "bottom":1},
                                                    size_hint=(0.2, 0.1))
        self.float_layout.add_widget(self.back_to_menu_button)

        # Create a grid layout inside the float layout.
        self.grid_layout = GridLayout(rows=4,
                                      cols=3,
                                      pos_hint={"center_x":0.5, "bottom":0},
                                      size_hint=(0.5, 0.7))
        self.float_layout.add_widget(self.grid_layout)

        # Inside the grid layout, create the sliders.
        self.current_slider = Slider(id="current_slider",
                                     min=0.1,
                                     max=900,
                                     step=0.1,
                                     orientation='vertical',
                                     pos_hint={"x":0.5, "top":0.3},
                                     size_hint=(0.1, 0.6),
                                     value=0.1,
                                     value_track=True,
                                     value_track_color=[0.404, 0.227, 0.718, 1.0],
                                     disabled=True)
        self.current_slider.bind(value=self.calculate_ohm_values)
        self.grid_layout.add_widget(self.current_slider)

        self.voltage_slider = Slider(id="voltage_slider",
                                     min=0.1,
                                     max=9,
                                     step=0.1,
                                     orientation='vertical',
                                     pos_hint={"x":0.5, "top":0.3},
                                     size_hint=(0.1, 0.6),
                                     value_track=True,
                                     value_track_color=[0.404, 0.227, 0.718, 1.0],
                                     value=0.05)
        self.grid_layout.add_widget(self.voltage_slider)
        self.voltage_slider.bind(value=self.calculate_ohm_values)

        self.resistance_slider = Slider(id="resistance_slider",
                                        min=10,
                                        max=1000,
                                        step=0.1,
                                        orientation='vertical',
                                        pos_hint={"x":0.5, "top":0.3},
                                        size_hint=(0.1, 0.6),
                                        value_track=True,
                                        value_track_color=[0.404, 0.227, 0.718, 1.0],
                                        value=500)
        self.grid_layout.add_widget(self.resistance_slider)
        self.resistance_slider.bind(value=self.calculate_ohm_values)

        # Inside the grid layout, create the labels.
        self.current_label = Label(text=str(self.current_slider.value) + "\nmA",
                                   size_hint=(0.1, 0.1),
                                   halign='center')
        self.grid_layout.add_widget(self.current_label)
        self.voltage_label = Label(text=str(self.voltage_slider.value) + "\nV",
                                   size_hint=(0.1, 0.1),
                                   halign='center')
        self.grid_layout.add_widget(self.voltage_label)
        self.resistance_label = Label(text=str(self.resistance_slider.value) + "\nOhms",
                                      size_hint=(0.1, 0.1),
                                      halign='center')
        self.grid_layout.add_widget(self.resistance_label)

        # Outside the grid layout (but inside the float layout), add the reset button.
        reset_ohm_button = ResetOhmButton(pos_hint={"right":1, "bottom":1},
                                          size_hint=(0.2, 0.1))
        self.float_layout.add_widget(reset_ohm_button)


    def deactivate_sliders(self, instance):
        """
        Deactivate the slider corresponding to the selection option.
        """
        if instance.id == "triangle_bottom_left_button":
            # Change the background image of the triangle.
            self.triangle_image.source = "assets/images/I_318px-law_triangle.png"
            self.selected = "current"
            # Activate and deactivate sliders accordingly.
            self.current_slider.disabled = True
            self.voltage_slider.disabled = False
            self.resistance_slider.disabled = False
            # Set minimum and maximum values for sliders
            # (in order for ranges to make sense).
            self.current_slider.max = 900
            self.current_slider.min = 0.1
            self.voltage_slider.max = 9
            self.voltage_slider.min = 0.1
            self.resistance_slider.max = 1000
            self.resistance_slider.min = 10
        elif instance.id == "triangle_top_left_button" or \
        instance.id == "triangle_top_right_button":
            # Change the background image of the triangle.
            self.triangle_image.source = "assets/images/V_318px-law_triangle.png"
            self.selected = "voltage"
            # Activate and deactivate sliders accordingly.
            self.current_slider.disabled = False
            self.voltage_slider.disabled = True
            self.resistance_slider.disabled = False
            # Set minimum and maximum values for sliders
            # (in order for ranges to make sense).
            self.current_slider.max = 900
            self.current_slider.min = 0.1
            self.voltage_slider.max = 900
            self.voltage_slider.min = 0
            self.resistance_slider.max = 1000
            self.resistance_slider.min = 10
        elif instance.id == "triangle_bottom_right_button":
            # Change the background image of the triangle.
            self.triangle_image.source = "assets/images/R_318px-law_triangle.png"
            self.selected = "resistance"
            # Activate and deactivate sliders accordingly.
            self.current_slider.disabled = False
            self.voltage_slider.disabled = False
            self.resistance_slider.disabled = True
            # Set minimum and maximum values for sliders
            # (in order for ranges to make sense).
            self.current_slider.max = 900
            self.current_slider.min = 100
            self.voltage_slider.max = 100
            self.voltage_slider.min = 1
            self.resistance_slider.max = 1000
            self.resistance_slider.min = 1

    def calculate_ohm_values(self, instance, value):
        """Calculate values according to the currently selected option."""
        if self.selected == "current":
            self.current_slider.value = \
                (self.voltage_slider.value / self.resistance_slider.value) * 1000
        elif self.selected == "voltage":
            self.voltage_slider.value = \
                (self.current_slider.value / 1000) * self.resistance_slider.value
        elif self.selected == "resistance":
            self.resistance_slider.value = \
                self.voltage_slider.value / self.current_slider.value * 1000

        # Update the text in the labels to show the current value(s).
        self.current_label.text = str(round(self.current_slider.value, 2)) + "\nmA"
        self.voltage_label.text = str(round(self.voltage_slider.value, 2)) + "\nV"
        self.resistance_label.text = str(round(self.resistance_slider.value, 2)) + "\nOhms"


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
        self.screen_manager.add_widget(OhmScreen(name="ohm_screen"))
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
        """
        Hook the keyboard to listen to its behaviour.
        """
        EventLoop.window.bind(on_keyboard=self.hook_keyboard)


    def hook_keyboard(self, window, key, *largs):
        """
        Capture behavior for the "back" button in Android.
        """
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
