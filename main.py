#!/usr/bin/env python
"""A mobile educational application about electricity and magnetism."""

# Operating System functionality.
import os

# Shuffle answers in quizzes to confuse students.
import random

# SQLite connections and retrieval.
import sqlite3

# GUI
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

# Animation
from kivy.animation import Animation

import kivy
kivy.require('1.11.1')


class MenuScreen(Screen):
    """
    Custom Menu Screen.

    It inherits from Screen.
    """


class MenuScreenButton(Button):
    """
    Custom button style for the Menu Screen.

    It inherits from kivy.uix.button.
    """


class PurpleRoundedButton(Button):
    """
    Custom button style for the "back to menu" and "reset" buttons.

    It inherits from kivy.uix.button.
    """


class WhiteRoundedButton(Button):
    """
    Custom button style for the "back to menu" and "reset" buttons.

    It inherits from kivy.uix.button.
    """


class QuestionLabel(Label):
    """
    Custom Label that wraps its text in case it is too long.

    It inherits from from kivy.uix.label
    """


class StudyInstructionsPopup(Popup):
    """
    Custom PopUp to show usage instructions.

    It inherits from from kivy.uix.popup
    """


class QuizInstructionsPopup(Popup):
    """
    Custom PopUp to show usage instructions.

    It inherits from from kivy.uix.popup
    """


class OhmInstructionsPopup(Popup):
    """
    Custom PopUp to show usage instructions.

    It inherits from from kivy.uix.popup
    """


class BackToMenuButton(PurpleRoundedButton):
    """
    Custom button style to go back to the Menu Screen.

    It inherits from kivy.uix.button.
    """


class ResetButton(PurpleRoundedButton):
    """
    Custom reset button.

    It inherits from PurpleRoundedButton.
    """


class InstructionsButton(PurpleRoundedButton):
    """
    Custom instructions button.

    It inherits from PurpleRoundedButton.
    """


class SettingsButton(MenuScreenButton):
    """
    Custom Settings button style for the Menu Screen.

    It inherits from MenuScreenButton, which inherits from kivy.uix.button.
    """


class AboutButton(MenuScreenButton):
    """
    Custom "About" button style for the Menu Screen.

    It inherits from MenuScreenButton, which inherits from kivy.uix.button.
    """


class AboutScreen(Screen):
    """
    Custom Screen Class for the About section.

    It inherits from Screen.
    """


class ResetQuizButton(ResetButton):
    """
    Custom reset button for the Quiz screen.

    It inherits from kivy.uix.button.
    """
    def on_press(self):
        """
        Set the Sliders values to their defaults.
        """
        # Reset the counters.
        self.parent.parent.correct_questions_counter = 0
        self.parent.parent.incorrect_questions_counter = 0
        self.parent.parent.result_label.color = (0, 0, 0, 0)
        self.parent.parent.correct_question_counter_label.font_size = "15sp"
        self.parent.parent.correct_question_counter_label.color = (1, 1, 1, 1)
        self.parent.parent.incorrect_question_counter_label.font_size = "15sp"
        self.parent.parent.incorrect_question_counter_label.color = (1, 1, 1, 1)

        # Re-draw the answers counters.
        self.parent.parent.correct_question_counter_label.text = \
            str(self.parent.parent.correct_questions_counter)
        self.parent.parent.incorrect_question_counter_label.text = \
            str(self.parent.parent.incorrect_questions_counter)


class ResetOhmButton(ResetButton):
    """
    Custom reset button for the Ohm screen.

    It inherits from kivy.uix.button.
    """
    def on_press(self):
        """Set the Sliders values to their defaults."""
        # Reset to the default image.
        self.parent.parent.triangle_image.source = \
            "assets/images/I_318px-law_triangle.png"
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
        self.rst_document = RstDocument(source="assets/chapters/english/chapter01.rst",
                                        show_errors=True,
                                        size_hint=(0.8, 1),
                                        pos_hint={"right":1, "top":1})
        self.float_layout.add_widget(self.rst_document)

        # Add the dropdown "menu" at the left of the screen.
        self.dropdown = DropDown()
        for chapter in ['01', '02', '03']:
            # when adding widgets, we need to specify the height manually
            # (disabling the size_hint_y) so the dropdown can calculate the
            # area it needs.
            btn = PurpleRoundedButton(text=chapter,
                                      height=400,
                                      #height=0.2,
                                      size_hint_y=None)

            # For each button, attach a callback that will call the select()
            # method on the dropdown. We'll pass the text of the button as
            # the data of the selection.
            btn.bind(on_release=lambda btn: self.dropdown.select(btn.text))
            # Add another bind so the RST document is updated according to
            # the selection.
            btn.bind(on_press=lambda btn: self.update_study_text(btn.text))

            # Add the button inside the dropdown.
            self.dropdown.add_widget(btn)

        # Create a big main button to open the dropdown.
        self.mainbutton = PurpleRoundedButton(text='Lessons',
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

        # Add a button explaining how to use this section.
        self.study_instructions_button = \
            InstructionsButton(pos_hint={"center_x": 0.1, "bottom": 1})
        self.study_instructions_button.bind(on_press=self.show_instructions)
        self.float_layout.add_widget(self.study_instructions_button)

    def show_instructions(self, instance):
        """Display instructions for this section."""
        popup = StudyInstructionsPopup()
        popup.open()

    def update_study_text(self, chapter):
        """
        Update the text in the RST widget according to the dropdown selection.
        """
        self.rst_document.source = \
            "assets/chapters/english/chapter" + chapter.replace("'", "") + ".rst"


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
        self.correct_questions_counter = 0
        self.incorrect_questions_counter = 0

        # Create a float layout.
        self.float_layout = FloatLayout()
        self.add_widget(self.float_layout)

        # Add a button explaining how to use this section.
        self.quiz_instructions_button = \
            InstructionsButton(pos_hint={"center_x": 0.1, "bottom": 1})
        self.quiz_instructions_button.bind(on_press=self.show_instructions)
        self.float_layout.add_widget(self.quiz_instructions_button)

        # A label to show "Correct!" or "Incorrect!"
        # depending on the selected answer.
        self.result_label = Label(text="",
                                  size_hint=(0.5, 0.05),
                                  color=(0, 0, 0, 0),
                                  pos_hint={"center_x": 0.5, "top": 0.95})
        self.float_layout.add_widget(self.result_label)

        # Labels for correct/incorrect questions counters.
        # Create a grid layout for the correct/incorrect display.
        self.answers_counters_grid_layout = \
            GridLayout(rows=2, cols=2,
                       pos_hint={"top":0.95, "right": 0.95},
                       #size=(200, 200),
                       #size_hint=(None, None)
                       size_hint=(0.2, 0.1))

        correct_answer_icon = Image(source="assets/icons/ic_check_white_48dp.png",
                                    keep_ratio=True,
                                    #size_hint=(0.01, 0.01),
                                    #size_hint=(None, None),
                                    #width=100,
                                    #height=100,
                                    allow_stretch=True)
        self.answers_counters_grid_layout.add_widget(correct_answer_icon)

        # Add the correct question counter label to the grid layout.
        self.correct_question_counter_label = \
            Label(text=str(self.correct_questions_counter), font_size="20sp")
        self.answers_counters_grid_layout.add_widget(
            self.correct_question_counter_label)

        incorrect_answer_icon = Image(source="assets/icons/ic_close_white_48dp.png",
                                      keep_ratio=True,
                                      allow_stretch=True)
        self.answers_counters_grid_layout.add_widget(incorrect_answer_icon)

        # Add the incorrect question counter label to the grid layout.
        self.incorrect_question_counter_label = \
            Label(text=str(self.incorrect_questions_counter),
                  font_size="20sp")
        self.answers_counters_grid_layout.add_widget(
            self.incorrect_question_counter_label)

        # Add the grid layout to the float layout.
        self.float_layout.add_widget(self.answers_counters_grid_layout)

        # Question label
        self.question_label = QuestionLabel(halign="center",
                                            valign="middle",
                                            font_size="15sp",
                                            pos_hint={"center_x": 0.5,
                                                      "top": 0.9})
        self.float_layout.add_widget(self.question_label)

        # Create a box layout inside the float layout (to contain the answer
        # buttons).
        self.answers_box_layout = BoxLayout(orientation="vertical",
                                            spacing=20,
                                            pos_hint={"center_x":0.5,
                                                      "top":0.7},
                                            size_hint=(0.5, 0.6))
        self.float_layout.add_widget(self.answers_box_layout)

        # Outside the grid layout (but inside the float layout), add the
        # reset button.
        reset_quiz_button = ResetQuizButton(pos_hint={"right":1, "bottom":1},
                                            size_hint=(0.2, 0.1))
        self.float_layout.add_widget(reset_quiz_button)

        # Connect to the SQLite DB and create a cursor.
        project_dir = os.path.dirname(os.path.realpath(__file__))
        connection = sqlite3.connect(os.path.join(os.sep, project_dir,
                                                  "db", "questions.db"))
        self.cursor = connection.cursor()

        # No questions have been retrieved yet.
        self.last_question_id = ""

        # Get a random question from the DB and display it.
        self.get_random_question()

    def show_instructions(self, instance):
        """Display instructions for this section."""
        popup = QuizInstructionsPopup()
        popup.open()

    def get_random_question(self):
        """Retrieve data from the SQLite DB."""
        # Get a random question, but not the previous question!
        self.cursor.execute(
            "SELECT * FROM questions "
            f"WHERE question_id NOT IN ('{self.last_question_id}') "
            "ORDER BY RANDOM() LIMIT 1")
        # "Fetch all" returns a list with a tuple.
        question = self.cursor.fetchall()
        self.last_question_id = str(question[0][0])

        # Show the question text into the question label.
        self.question_label.text = str(question[0][1])

        # Get answers to this question, and display them.
        self.get_answers()

    def get_answers(self):
        """Get the corresponding answers for the current question."""
        # Execute the query to get the answers to the current question.
        self.cursor.execute(
            "SELECT * FROM answers "
            "INNER JOIN questions "
            "ON questions.question_id = answers.question_id "
            f"WHERE questions.question_text = '{self.question_label.text}'")
        # "Fetch all" returns a list with a tuple.
        answers = self.cursor.fetchall()

        # Get the correct answer.
        self.cursor.execute(
            "SELECT answer_text FROM answers "
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
            answer_button = WhiteRoundedButton(text=answer)

            # For each button, attach a callback that will call the
            # check_answer method.
            # We'll pass the text of the button as the data of the selection.
            answer_button.bind(on_release=lambda answer_button:
                               self.check_answer(answer_button.text))

            # Add the button inside the box layout for the answers.
            self.answers_box_layout.add_widget(answer_button)

    def animate_scoreboard(self, object_to_animate):
        animation = Animation(color=(1, 1, 0, 1.0),
                              duration=0.1) & \
                    Animation(font_size=object_to_animate.font_size+10,
                              duration=0.1) + \
                    Animation(color=object_to_animate.color,
                              duration=0.1) + \
                    Animation(font_size=object_to_animate.font_size,
                              duration=0.1)
        # Start the animation.
        animation.start(object_to_animate)

    def animate_result_notification(self, result):
        # Change the result notification text accordingly.
        self.result_label.text = result

        if result == "Wrong":
            # Change text color to red.
            animation = Animation(color=(1, 0, 0, 1),
                                  duration=0.1) & \
                        Animation(font_size=self.result_label.font_size+20,
                                  duration=0.1) + \
                        Animation(color=self.result_label.color,
                                  duration=0.5) + \
                        Animation(font_size=self.result_label.font_size,
                                  duration=0.5)
        elif result == "Right!":
            # Change text color to green.
            animation = Animation(color=(0, 1, 0, 1), duration=0.1) & \
                        Animation(font_size=self.result_label.font_size+20,
                                  duration=0.1) + \
                        Animation(color=self.result_label.color,
                                  duration=0.5) + \
                        Animation(font_size=self.result_label.font_size,
                                  duration=0.5)
        animation.start(self.result_label)

    def check_answer(self, selected_answer):
        """Check if the selected answer is correct or not."""
        # "Reset" all the previous animations changes that may be already
        # running.
        self.result_label.font_size = "15sp"
        self.result_label.color = (0, 0, 0, 0)
        self.correct_question_counter_label.font_size = "20sp"
        self.correct_question_counter_label.color = (1, 1, 1, 1)
        self.incorrect_question_counter_label.font_size = "20sp"
        self.incorrect_question_counter_label.color = (1, 1, 1, 1)

        # Check if the selected answer is correct or not.
        if selected_answer == self.correct_answer:
            # Increment the correct answer counter.
            self.correct_questions_counter += 1
            # Start animations.
            self.animate_scoreboard(self.correct_question_counter_label)
            self.animate_result_notification("Right!")
        else:
            # Increment the incorrect answer counter.
            self.incorrect_questions_counter += 1
            # Start animations.
            self.animate_scoreboard(self.incorrect_question_counter_label)
            self.animate_result_notification("Wrong")

        # Re-draw the answers counters.
        self.correct_question_counter_label.text = \
            str(self.correct_questions_counter)
        self.incorrect_question_counter_label.text = \
            str(self.incorrect_questions_counter)

        # Destroy the answer buttons (to prepare for the new ones).
        self.answers_box_layout.clear_widgets()

        # Call the get_random_question method again.
        self.get_random_question()


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

        # Triangle image.
        self.triangle_image = Image(source="assets/images/I_318px-law_triangle.png",
                                    keep_ratio=False,
                                    #size_hint=(0.2, 0.2),
                                    size_hint=(None, None),
                                    width="150sp",
                                    height="150sp",
                                    allow_stretch=True,
                                    pos_hint={"center_x": 0.5, "top": 0.97})
        self.float_layout.add_widget(self.triangle_image)

        # Invisible grid layout and buttons for the triangle image.
        triangle_grid_layout = GridLayout(rows=2, cols=2,
                                          pos_hint={"center_x":0.5,
                                                    "top": 0.97},
                                          size=("150sp", "150sp"),
                                          size_hint=(None, None))
        triangle_top_left_button = Button(id="triangle_top_left_button",
                                          size_hint_x=None, width="75sp",
                                          size_hint_y=None, height="75sp",
                                          opacity=0)
        triangle_top_left_button.bind(on_press=self.deactivate_sliders)
        triangle_grid_layout.add_widget(triangle_top_left_button)

        triangle_top_right_button = Button(id="triangle_top_right_button",
                                           size_hint_x=None, width="75sp",
                                           size_hint_y=None, height="75sp",
                                           background_color=(0, 0, 0, 0),
                                           background_normal="")
        triangle_top_right_button.bind(on_press=self.deactivate_sliders)
        triangle_grid_layout.add_widget(triangle_top_right_button)

        triangle_bottom_left_button = Button(id="triangle_bottom_left_button",
                                             size_hint_x=None, width="75sp",
                                             size_hint_y=None, height="75sp",
                                             background_color=(0, 0, 0, 0),
                                             background_normal="")
        triangle_bottom_left_button.bind(on_press=self.deactivate_sliders)
        triangle_grid_layout.add_widget(triangle_bottom_left_button)

        triangle_bottom_right_button = Button(id="triangle_bottom_right_button",
                                              size_hint_x=None, width="75sp",
                                              size_hint_y=None, height="75sp",
                                              background_color=(0, 0, 0, 0),
                                              background_normal="")
        triangle_bottom_right_button.bind(on_press=self.deactivate_sliders)
        triangle_grid_layout.add_widget(triangle_bottom_right_button)
        self.float_layout.add_widget(triangle_grid_layout)

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
                                     pos_hint={"x": 0.5, "top": 0.3},
                                     size_hint=(0.1, 0.6),
                                     value=0.1,
                                     value_track=True,
                                     value_track_color=(1, 0.96, 0.49, 1.0),
                                     disabled=True)
        self.current_slider.bind(value=self.calculate_ohm_values)
        self.grid_layout.add_widget(self.current_slider)

        self.voltage_slider = Slider(id="voltage_slider",
                                     min=0.1,
                                     max=9,
                                     step=0.1,
                                     orientation='vertical',
                                     pos_hint={"x": 0.5, "top": 0.3},
                                     size_hint=(0.1, 0.6),
                                     value_track=True,
                                     value_track_color=(1, 0.96, 0.49, 1.0),
                                     value=0.05)
        self.grid_layout.add_widget(self.voltage_slider)
        self.voltage_slider.bind(value=self.calculate_ohm_values)

        self.resistance_slider = Slider(id="resistance_slider",
                                        min=10,
                                        max=1000,
                                        step=0.1,
                                        orientation='vertical',
                                        pos_hint={"x": 0.5, "top": 0.3},
                                        size_hint=(0.1, 0.6),
                                        value_track=True,
                                        value_track_color=(1, 0.96, 0.49, 1.0),
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

        # Add a button explaining how to use this section.
        self.ohm_instructions_button = \
            InstructionsButton(pos_hint={"center_x": 0.1, "bottom": 1})
        self.ohm_instructions_button.bind(on_press=self.show_instructions)
        self.float_layout.add_widget(self.ohm_instructions_button)

        # Outside the grid layout (but inside the float layout), add the
        # reset button.
        reset_ohm_button = ResetOhmButton(pos_hint={"right": 1, "bottom": 1},
                                          size_hint=(0.2, 0.1))
        self.float_layout.add_widget(reset_ohm_button)

    def show_instructions(self, instance):
        """Display instructions for this section."""
        popup = OhmInstructionsPopup()
        popup.open()

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
        self.current_label.text = \
            str(round(self.current_slider.value, 2)) + "\nmA"
        self.voltage_label.text = \
            str(round(self.voltage_slider.value, 2)) + "\nV"
        self.resistance_label.text = \
            str(round(self.resistance_slider.value, 2)) + "\nOhms"


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

    def post_build_init(self, event):
        """Hook the keyboard to listen to its behavior."""
        EventLoop.window.bind(on_keyboard=self.hook_keyboard)

    def hook_keyboard(self, window, key, *largs):
        """Capture behavior for the "back" button in Android."""
        # Key 27 is "Esc" in the Keyboard, or "Back" on Android.
        if key == 27:
            print(self.screen_manager.current)
            if self.screen_manager.current == 'menu_screen':
                Gilbert.get_running_app().stop()
            self.screen_manager.transition.direction = "right"
            if isinstance(self.screen_manager.previous, str):
                self.screen_manager.current = self.screen_manager.previous
            else:
                self.screen_manager.current = self.screen_manager.previous()
            return_value = True
        else:
            return_value = False
        return return_value

    def build_config(self, config):
        """Set the default values for the configs sections."""
        config.setdefaults('MenuScreenButton', {'font_size': "15sp"})

    def build_settings(self, settings):
        """
        Add our custom section to the default configuration object.
        """
        # We use the string defined above for our config JSON, but it could
        # also be loaded from a file as follows:
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
                SettingsButton.font_size = float(value)

    def close_settings(self, settings=None):
        """
        The settings panel has been closed.
        """
        Logger.info("main.py: App.close_settings: %s", settings)
        super(Gilbert, self).close_settings(settings)


if __name__ == "__main__":
    Gilbert().run()
