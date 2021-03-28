#!/usr/bin/env python
"""A mobile educational application about electricity and magnetism."""

# Operating System functionality.
import os

# Shuffle answers in quizzes to confuse students.
import random

import sympy

# SQLite connections and retrieval.
import sqlite3

# Electrical circuits calculations.
#from dcelectricity.dc_en import *

# GUI
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.slider import Slider
from kivy.uix.dropdown import DropDown
from kivy.uix.textinput import TextInput
from kivy.uix.checkbox import CheckBox
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


class OhmCalcInstructionsPopup(Popup):
    """
    Custom PopUp to show usage instructions.

    It inherits from from kivy.uix.popup
    """


class KirchhoffInstructionsCarouselPopup(Popup):
    """
    Custom PopUp to show usage instructions.

    It inherits from from kivy.uix.popup
    """


class KirchhoffExamplesCarouselPopup(Popup):
    """
    Custom PopUp to show usage instructions.

    It inherits from from kivy.uix.popup
    """


class KirchhoffFormulasPopup(Popup):
    """
    Custom PopUp to show formulas.

    It inherits from from kivy.uix.popup
    """


class OhmMissingValuesPopup(Popup):
    """
    Custom PopUp to a warning about missing required values.

    It inherits from from kivy.uix.popup
    """


class KirchhoffPopup(Popup):
    """
    Custom PopUp to a warning in the Kirchhoff screen.

    It inherits from from kivy.uix.popup
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
        """Set the Sliders values to their defaults."""
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


class ResetCalcButton(WhiteRoundedButton):
    """
    Custom reset button for the Calculator screen.

    It inherits from kivy.uix.button.
    """

    def on_press(self):
        """Set the Sliders values to their defaults."""
        # Reset the inputs.
        inputs_list = [self.parent.parent.parent.ohm_input,
                       self.parent.parent.parent.amp_input,
                       self.parent.parent.parent.volt_input]
        for input in inputs_list:
            input.text = ""


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
        """Class constructor."""
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
                                              pos_hint={"left": 0, "top": 1})

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
        """Update the text in the RST widget according to the dropdown selection."""
        self.rst_document.source = \
            "assets/chapters/english/chapter" + chapter.replace("'", "") + ".rst"


class QuizScreen(Screen):
    """
    Custom Screen Class for the Quiz section.

    It inherits from Screen.
    """

    def __init__(self, **kwargs):
        """Class constructor."""
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
                       pos_hint={"top": 0.95, "right": 0.95},
                       size_hint=(0.2, 0.1))

        correct_answer_icon = Image(source="assets/icons/ic_check_white_48dp.png",
                                    keep_ratio=True,
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
                                            pos_hint={"center_x": 0.5,
                                                      "top": 0.7},
                                            size_hint=(0.5, 0.6))
        self.float_layout.add_widget(self.answers_box_layout)

        # Outside the grid layout (but inside the float layout), add the
        # reset button.
        reset_quiz_button = ResetQuizButton(pos_hint={"right": 1, "bottom": 1},
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
            "AND language = 'english'"
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


class KirchhoffScreen(Screen):
    """
    Custom Screen Class for Kirchhoff study.

    It inherits from Screen.
    """

    def __init__(self, **kwargs):
        """Class constructor."""
        super(KirchhoffScreen, self).__init__(**kwargs)

        # Create a float layout.
        self.float_layout = FloatLayout()
        self.add_widget(self.float_layout)

        # Add the circuit image.
        self.circuit_image = Image(source="assets/images/circuit_tall.png",
                                   keep_ratio=False,
                                   size_hint=(0.6, 0.55),
                                   allow_stretch=True,
                                   pos_hint={"center_x": 0.5, "top": 0.8})
        self.float_layout.add_widget(self.circuit_image)

        # Add a box layout for the V1 Label+input combo (to make it easier
        # to move it all together).
        self.V1_box_layout = BoxLayout(orientation="horizontal",
                                       spacing=5,
                                       size_hint=(0.3, 0.05),
                                       pos_hint={"right": 0.4, "top": 0.8})
        # Voltage 1 label.
        self.V1_label = Label(text="V1=",
                              size_hint_x=0.5,
                              pos_hint={'right': 1})
        self.V1_box_layout.add_widget(self.V1_label)
        # Add the grid layout to the general float layout.
        self.float_layout.add_widget(self.V1_box_layout)
        # Voltage 1 input box.
        self.V1_input = TextInput(font_size="18sp",
                                  input_type="number",
                                  multiline=False,
                                  input_filter="float",
                                  halign='center',
                                  id="V1")
        self.V1_box_layout.add_widget(self.V1_input)
        # Voltage 1 units label.
        self.V1_units_label = Label(text="V",
                                    size_hint_x=0.15,
                                    pos_hint={'left': 1})
        self.V1_box_layout.add_widget(self.V1_units_label)

        # Add a box layout for the V2 Label+input combo (to make it easier
        # to move it all together).
        self.V2_box_layout = BoxLayout(orientation="horizontal",
                                       spacing=5,
                                       size_hint=(0.2, 0.05),
                                       pos_hint={"right": 0.55, "top": 0.6})
        # Voltage 2 label.
        self.V2_label = Label(text="V2=",
                              size_hint_x=0.5,
                              pos_hint={'right': 1})
        self.V2_box_layout.add_widget(self.V2_label)
        # Add the grid layout to the general float layout.
        self.float_layout.add_widget(self.V2_box_layout)
        # Voltage 2 input box.
        self.V2_input = TextInput(font_size="18sp",
                                  input_type="number",
                                  multiline=False,
                                  input_filter="float",
                                  halign='center',
                                  id="V2")
        self.V2_input.bind(text=self.v2v3_equality)
        self.V2_box_layout.add_widget(self.V2_input)
        # Voltage 2 units label.
        self.V2_units_label = Label(text="V",
                                    size_hint_x=0.15,
                                    pos_hint={'left': 1})
        self.V2_box_layout.add_widget(self.V2_units_label)

        # Add a box layout for the V3 Label+input combo (to make it easier
        # to move it all together).
        self.V3_box_layout = BoxLayout(orientation="horizontal",
                                       spacing=5,
                                       size_hint=(0.2, 0.05),
                                       pos_hint={"right": 0.98, "top": 0.6})
        self.float_layout.add_widget(self.V3_box_layout)
        # Voltage 3 label.
        self.V3_label = Label(text="V3=",
                              size_hint_x=0.5,
                              pos_hint={'right': 1},
                              markup=True)
        self.V3_box_layout.add_widget(self.V3_label)
        # Voltage 3 input box.
        self.V3_input = TextInput(font_size="18sp",
                                  input_type="number",
                                  multiline=False,
                                  input_filter="float",
                                  halign='center',
                                  id="V3")
        self.V3_input.bind(text=self.v2v3_equality)
        self.V3_box_layout.add_widget(self.V3_input)
        # Voltage 3 units label.
        self.V3_units_label = Label(text="V",
                                    size_hint_x=0.15,
                                    pos_hint={'left': 1})
        self.V3_box_layout.add_widget(self.V3_units_label)

        # Add a box layout for the V4 Label+input combo (to make it easier
        # to move it all together).
        self.V4_box_layout = BoxLayout(orientation="horizontal",
                                       spacing=5,
                                       size_hint=(0.3, 0.05),
                                       pos_hint={"right": 0.4, "top": 0.3})
        self.float_layout.add_widget(self.V4_box_layout)
        # Voltage 4 label.
        self.V4_label = Label(text="V4=",
                              size_hint_x=0.5,
                              pos_hint={'right': 1},
                              markup=True)
        self.V4_box_layout.add_widget(self.V4_label)
        # Voltage 4 input box.
        self.V4_input = TextInput(font_size="18sp",
                                  input_type="number",
                                  multiline=False,
                                  input_filter="float",
                                  halign='center',
                                  id="V4",
                                  disabled=True)
        self.V4_box_layout.add_widget(self.V4_input)
        # Voltage 4 units label.
        self.V4_units_label = Label(text="V",
                                    size_hint_x=0.15,
                                    pos_hint={'left': 1})
        self.V4_box_layout.add_widget(self.V4_units_label)

        # Add a box layout for the I1 Label+input combo (to make it easier
        # to move it all together).
        self.I1_box_layout = BoxLayout(orientation="horizontal",
                                       spacing=5,
                                       size_hint=(0.3, 0.05),
                                       pos_hint={"right": 0.8, "top": 0.8})
        self.float_layout.add_widget(self.I1_box_layout)
        # Current 1 label.
        self.I1_label = Label(text="I1=",
                              size_hint_x=0.2,
                              pos_hint={'right': 1})
        self.I1_box_layout.add_widget(self.I1_label)
        # Current 1 input box.
        self.I1_input = TextInput(font_size="18sp",
                                  input_type="number",
                                  multiline=False,
                                  input_filter="float",
                                  halign='center',
                                  id="I1")
        self.I1_box_layout.add_widget(self.I1_input)
        # Current 1 units label.
        self.I1_units_label = Label(text="A",
                                    size_hint_x=0.15,
                                    pos_hint={'left': 1})
        self.I1_box_layout.add_widget(self.I1_units_label)

        # Add a box layout for the I2 Label+input combo (to make it easier
        # to move it all together).
        self.I2_box_layout = BoxLayout(orientation="horizontal",
                                       spacing=5,
                                       size_hint=(0.2, 0.05),
                                       pos_hint={"right": 0.55, "top": 0.5})
        self.float_layout.add_widget(self.I2_box_layout)
        # Resistance 2 label.
        self.I2_label = Label(text="I2=",
                              size_hint_x=0.25,
                              pos_hint={'right': 1})
        self.I2_box_layout.add_widget(self.I2_label)
        # Resistance 2 input box.
        self.I2_input = TextInput(font_size="18sp",
                                  input_type="number",
                                  multiline=False,
                                  input_filter="float",
                                  halign='center',
                                  id="I2")
        self.I2_box_layout.add_widget(self.I2_input)
        # Current 2 units label.
        self.I2_units_label = Label(text="A",
                                    size_hint_x=0.15,
                                    pos_hint={'left': 1})
        self.I2_box_layout.add_widget(self.I2_units_label)

        # Add a box layout for the I3 Label+input combo (to make it easier
        # to move it all together).
        self.I3_box_layout = BoxLayout(orientation="horizontal",
                                       spacing=5,
                                       size_hint=(0.2, 0.05),
                                       pos_hint={"right": 0.98, "top": 0.5})
        self.float_layout.add_widget(self.I3_box_layout)
        # Resistance 3 label.
        self.I3_label = Label(text="I3=",
                              size_hint_x=0.25,
                              pos_hint={'right': 1})
        self.I3_box_layout.add_widget(self.I3_label)
        # Resistance 3 input box.
        self.I3_input = TextInput(font_size="18sp",
                                  input_type="number",
                                  multiline=False,
                                  input_filter="float",
                                  halign='center',
                                  id="I3")
        self.I3_box_layout.add_widget(self.I3_input)
        # Current 3 units label.
        self.I3_units_label = Label(text="A",
                                    size_hint_x=0.15,
                                    pos_hint={'left': 1})
        self.I3_box_layout.add_widget(self.I3_units_label)

        # Add a box layout for the I4 Label+input combo (to make it easier
        # to move it all together).
        self.I4_box_layout = BoxLayout(orientation="horizontal",
                                       spacing=5,
                                       size_hint=(0.3, 0.05),
                                       pos_hint={"right": 0.8, "top": 0.3})
        self.float_layout.add_widget(self.I4_box_layout)
        # Current 4 label.
        self.I4_label = Label(text="I4=",
                              size_hint_x=0.25,
                              pos_hint={'right': 1})
        self.I4_box_layout.add_widget(self.I4_label)
        # Current 4 input box.
        self.I4_input = TextInput(font_size="18sp",
                                  input_type="number",
                                  multiline=False,
                                  input_filter="float",
                                  halign='center',
                                  disabled=True,
                                  id="I4")
        self.I4_box_layout.add_widget(self.I4_input)
        # Current 4 units label.
        self.I4_units_label = Label(text="A",
                                    size_hint_x=0.15,
                                    pos_hint={'left': 1})
        self.I4_box_layout.add_widget(self.I4_units_label)

        # Add a box layout for the VT Label+input combo (to make it easier
        # to move it all together).
        self.VT_box_layout = BoxLayout(orientation="horizontal",
                                       spacing=5,
                                       size_hint=(0.2, 0.05),
                                       pos_hint={"right": 0.23, "top": 0.55})
        self.float_layout.add_widget(self.VT_box_layout)
        # VT label.
        self.VT_label = Label(text="VT=",
                              size_hint_x=0.5,
                              pos_hint={'right': 1})
        self.VT_box_layout.add_widget(self.VT_label)
        # VT input box.
        self.VT_input = TextInput(font_size="18sp",
                                  input_type="number",
                                  multiline=False,
                                  input_filter="float",
                                  halign='center',
                                  id="VT")
        self.VT_box_layout.add_widget(self.VT_input)
        # Voltage T units label.
        self.VT_units_label = Label(text="V",
                                    size_hint_x=0.15,
                                    pos_hint={'left': 1})
        self.VT_box_layout.add_widget(self.VT_units_label)

        # Add a selection between the two Kirchhoff laws.
        self.laws_selection_layout = GridLayout(cols=2,
                                                rows=2,
                                                spacing=0,
                                                pos_hint={"center_x": 0.5,
                                                          "top": 0.95},
                                                size_hint=(0.9, 0.08))
        self.float_layout.add_widget(self.laws_selection_layout)

        # Add a radio button group with the 2 options.
        self.kirchhoff_current_checkbox = CheckBox()
        self.kirchhoff_current_checkbox.group = "option_kirchhoff"
        self.kirchhoff_current_checkbox.id = "current_checkbox"
        self.laws_selection_layout.add_widget(self.kirchhoff_current_checkbox)
        # Attach a callback.
        self.kirchhoff_current_checkbox.bind(active=self.on_checkbox_Active)

        self.kirchhoff_voltage_checkbox = CheckBox()
        self.kirchhoff_voltage_checkbox.group = "option_kirchhoff"
        self.kirchhoff_voltage_checkbox.id = "voltage_checkbox"
        self.laws_selection_layout.add_widget(self.kirchhoff_voltage_checkbox)
        # Attach a callback.
        self.kirchhoff_voltage_checkbox.bind(active=self.on_checkbox_Active)

        # Add a label for each radio button.
        current_label = Label(text="Current",
                              halign='center',
                              font_size="15sp")
        self.laws_selection_layout.add_widget(current_label)

        voltage_label = Label(text="Voltage",
                              halign='center',
                              font_size="15sp")
        self.laws_selection_layout.add_widget(voltage_label)
        # Add another grid layout for the buttons.
        self.buttons_grid_layout = GridLayout(cols=5,
                                              rows=1,
                                              spacing=10,
                                              pos_hint={"center_x": 0.5,
                                                        "bottom": 1},
                                              size_hint=(0.9, 0.1))
        self.float_layout.add_widget(self.buttons_grid_layout)

        # Add the instructions button.
        self.instructions_button = PurpleRoundedButton(text="Guide",
                                                       font_size="13sp")
        self.instructions_button.bind(on_press=self.show_instructions_carousel)
        self.buttons_grid_layout.add_widget(self.instructions_button)

        # Add the reset button.
        self.reset_button = ResetButton(text="Reset",
                                        font_size="13sp")
        self.reset_button.bind(on_press=self.reset_kirchhoff_values)
        self.buttons_grid_layout.add_widget(self.reset_button)

        # Add the formulas button.
        self.formulas_button = PurpleRoundedButton(text="Formulas",
                                                   font_size="13sp")
        self.formulas_button.bind(on_press=self.show_formulas)
        self.buttons_grid_layout.add_widget(self.formulas_button)

        # Add a "Example" button.
        self.example_button = PurpleRoundedButton(text="Example",
                                                  font_size="13sp")
        self.example_button.bind(on_press=self.show_example_carousel)
        self.buttons_grid_layout.add_widget(self.example_button)

        # Add a "Calculate" button.
        self.calculate_button = PurpleRoundedButton(text="Calculate",
                                                    font_size="13sp")
        self.calculate_button.bind(on_press=self.validate_inputs)
        self.buttons_grid_layout.add_widget(self.calculate_button)

        # Once all the items are in place, activate one of the
        # radio buttons by default.
        self.kirchhoff_current_checkbox.state = "down"

    def show_example_carousel(self, instance):
        """Show the example carousel popup."""
        popup = KirchhoffExamplesCarouselPopup()
        popup.open()

    def show_instructions_carousel(self, instance):
        """Display instructions for this section."""
        popup = KirchhoffInstructionsCarouselPopup()
        popup.open()

    def show_formulas(self, instance):
        """Display formulas for this section."""
        popup = KirchhoffFormulasPopup()
        popup.open()

    # Callback for the checkbox
    def on_checkbox_Active(self, checkboxInstance, isActive):
        """Deactivate the other two input fields and reset values."""
        if checkboxInstance.id == "voltage_checkbox":
            self.I1_input.disabled = True
            self.I2_input.disabled = True
            self.I3_input.disabled = True
            self.VT_input.disabled = False
            self.V1_input.disabled = False
            self.V2_input.disabled = False
            self.V3_input.disabled = False
        elif checkboxInstance.id == "current_checkbox":
            self.I1_input.disabled = False
            self.I2_input.disabled = False
            self.I3_input.disabled = False
            self.VT_input.disabled = True
            self.V1_input.disabled = True
            self.V2_input.disabled = True
            self.V3_input.disabled = True

    def v2v3_equality(self, instance, value):
        """On the key press, make sure V2 and V3 have the same text."""
        if instance.id == "V3":
            self.V2_input.text = self.V3_input.text
        else:
            self.V3_input.text = self.V2_input.text

    def validate_inputs(self, instance):
        """Validate appropiate inputs (before calculating results)."""
        # Check if the users wants to calculate Voltage or Current.
        if self.kirchhoff_voltage_checkbox.active:
            fields_to_check = [self.VT_input,
                               self.V1_input,
                               self.V2_input,
                               self.V3_input]
        else:
            fields_to_check = [self.I1_input]

        # A list to contain the IDs of the fields which are missing values.
        empty_fields = [field.id for field in fields_to_check if "" == field.text]
        # A list to contain the IDs of the fields with negative values.
        negative_fields = [field.id for field in fields_to_check if "-" in field.text]

        if empty_fields:
            message = f"Please enter a value in {', '.join(empty_fields)}"
            popup = KirchhoffPopup()
            popup.title = "Oops! One or more values are missing!"
            popup.label_text = message
            popup.open()
        elif negative_fields:
            message = f"Please enter a positive value in {', '.join(negative_fields)}"
            popup = KirchhoffPopup()
            popup.title = "Negative values are not allowed!"
            popup.label_text = message
            popup.open()
        elif self.kirchhoff_voltage_checkbox.active and \
            (float(self.V1_input.text) + float(self.V2_input.text)) > float(self.VT_input.text):
            message = f"The sum of [b]V1[/b] ({self.V1_input.text}), and " \
                      f"[b]V2[/b]/[b]V3[/b] ({self.V2_input.text}) cannot be greater " \
                      f"than [b]Vt[/b] ({self.VT_input.text})"
            popup = KirchhoffPopup()
            popup.title = "Invalid voltage."
            popup.label_text = message
            popup.open()
        elif self.kirchhoff_current_checkbox.active and \
            self.I2_input.text != "" and self.I3_input.text != "" and \
            (float(self.I2_input.text) + float(self.I3_input.text)) > float(self.I1_input.text):
            message = f"The sum of [b]I2[/b] ({self.I2_input.text}), and " \
                      f"[b]I3[/b]/[b]V3[/b] ({self.I3_input.text}) cannot be greater " \
                      f"than [b]I1[/b] ({self.I1_input.text})"
            popup = KirchhoffPopup()
            popup.title = "Invalid current."
            popup.label_text = message
            popup.open()
        else:
            # If there are no invalid fields, continue with the calculations.
            self.calculate_kirchhoff_values()

    def reset_kirchhoff_values(self, instance):
        """Reset all the values to their original status."""
        fields = [self.I1_input,
                  self.I2_input,
                  self.I3_input,
                  self.I4_input,
                  self.VT_input,
                  self.V1_input,
                  self.V2_input,
                  self.V3_input,
                  self.V4_input]

        for field in fields:
            field.text = ""

        self.kirchhoff_current_checkbox.state = "down"

    def calculate_kirchhoff_values(self):
        """Calculate values according to the currently selected option."""
        Vt, V1, V2, V3, V4, I1, I2, I3, I4 = \
            sympy.symbols('Vt, V1, V2, V3, V4, I1, I2, I3, I4')
        equations = []

        if self.kirchhoff_voltage_checkbox.active:
            Vt = float(self.VT_input.text)
            V1 = float(self.V1_input.text)
            if self.V2_input.text.isdigit() and self.V3_input.text == "":
                self.V3_input.text = self.V2_input.text
            if self.V3_input.text.isdigit() and self.V2_input.text == "":
                self.V2_input.text = self.V3_input.text
            V2 = float(self.V2_input.text)
            V3 = float(self.V3_input.text)
            equations.append(sympy.Eq(Vt - V1 - V3 - V4, 0))

            unknowns = [V4]
        elif self.kirchhoff_current_checkbox.active:
            I1 = float(self.I1_input.text)
            unknowns = [I4]

            if self.I1_input.text != "" and self.I2_input.text == "" and self.I3_input.text == "":
                message = "Please enter a value in either [b]I2[/b] or [b]I3[/b]."
                popup = KirchhoffPopup()
                popup.title = "Warning!"
                popup.separator_color = (1, 0, 0, 1)
                popup.label_text = message
                popup.open()

            if self.I2_input.text != "" and self.I3_input.text != "" and \
                (float(self.I2_input.text) + float(self.I3_input.text) != float(self.I1_input.text)):
                message = "The sum of I2 and I3 should be equal to I1.\n"\
                          "Please correct the values or delete one of "\
                          "them in order to calculate the other one."
                popup = KirchhoffPopup()
                popup.title = "Results:"
                popup.separator_color = (1, 0, 0, 1)
                popup.label_text = message
                popup.open()
            elif self.I2_input.text != "" and self.I3_input.text != "":
                I3 = float(self.I3_input.text)
                I2 = float(self.I2_input.text)
                equations.append(sympy.Eq(I4, I3 + I2))

            if self.I3_input.text == "" and self.I2_input.text != "":
                if float(self.I2_input.text) > float(self.I1_input.text):
                    message = "The sum of I2 and I3 should be equal to I1.\n"\
                              "Please correct the values or delete one of "\
                              "them in order to calculate the other one."
                    popup = KirchhoffPopup()
                    popup.title = "Warning!"
                    popup.separator_color = (1, 0, 0, 1)
                    popup.label_text = message
                    popup.open()
                else:
                    I2 = float(self.I2_input.text)
                    equations.append(sympy.Eq(I3, I1 - I2))
                    unknowns.append(I3)

            if self.I2_input.text == "" and self.I3_input.text != "":
                if float(self.I3_input.text) > float(self.I1_input.text):
                    message = "The sum of I2 and I3 should be equal to I1.\n"\
                              "Please correct the values or delete one of "\
                              "them in order to calculate the other one."
                    popup = KirchhoffPopup()
                    popup.title = "Warning!"
                    popup.separator_color = (1, 0, 0, 1)
                    popup.label_text = message
                    popup.open()
                else:
                    I3 = float(self.I3_input.text)
                    equations.append(sympy.Eq(I2, I1 - I3))
                    unknowns.append(I2)

        solutions = sympy.solve(equations, unknowns)

        if isinstance(solutions, dict):
            # If solutions is not a dict, it means no solutions were found.
            # So, let's not do anything.
            for k, v in solutions.items():
                solutions[k] = round(float(v), 3)

            if self.kirchhoff_voltage_checkbox.active:
                self.V4_input.text = str(solutions.get(V4, ""))
            if self.kirchhoff_current_checkbox.active:
                self.I4_input.text = str(solutions.get(I4, ""))
            if self.I3_input.text == "" and self.kirchhoff_current_checkbox.active:
                self.I3_input.text = str(solutions.get(I3, ""))
            if self.I2_input.text == "" and self.kirchhoff_current_checkbox.active:
                self.I2_input.text = str(solutions.get(I2, ""))

            solutions_text = ""
            for solution in solutions:
                solutions_text += f"{solution} = {solutions[solution]}\n"
            message = f"{solutions_text}"
            popup = KirchhoffPopup()
            popup.title = "Results:"
            popup.separator_color = (0, 1, 0, 1)
            popup.label_text = message
            popup.open()


class OhmCalcScreen(Screen):
    """
    Custom Screen Class for the Ohm's law calculator section.

    It inherits from Screen.
    """

    def __init__(self, **kwargs):
        """Class constructor."""
        super(OhmCalcScreen, self).__init__(**kwargs)

        # Create a float layout.
        self.float_layout = FloatLayout()
        self.add_widget(self.float_layout)

        self.option_label = Label(text="1 - Select an option to calculate:",
                                  pos_hint={"center_x": 0.5,
                                            "top": 0.95},
                                  size_hint=(0.9, 0.1))
        self.float_layout.add_widget(self.option_label)

        # Add a small grid layout for the V|I|R selection buttons
        # and their labels.
        self.radio_buttons_grid_layout = GridLayout(cols=3,
                                                    rows=3,
                                                    spacing=0,
                                                    pos_hint={"center_x": 0.5,
                                                              "top": 0.85},
                                                    size_hint=(0.9, 0.12))
        self.float_layout.add_widget(self.radio_buttons_grid_layout)

        # Add a radio button group with the 3 options.
        self.volt_checkbox = CheckBox()
        self.volt_checkbox.group = "option"
        self.volt_checkbox.id = "volt_checkbox"
        self.radio_buttons_grid_layout.add_widget(self.volt_checkbox)
        # Attach a callback.
        self.volt_checkbox.bind(active=self.on_checkbox_Active)

        self.amp_checkbox = CheckBox()
        self.amp_checkbox.group = "option"
        self.amp_checkbox.id = "amp_checkbox"
        self.radio_buttons_grid_layout.add_widget(self.amp_checkbox)
        # Attach a callback.
        self.amp_checkbox.bind(active=self.on_checkbox_Active)

        self.ohm_checkbox = CheckBox()
        self.ohm_checkbox.group = "option"
        self.ohm_checkbox.id = "ohm_checkbox"
        self.radio_buttons_grid_layout.add_widget(self.ohm_checkbox)
        # Attach a callback.
        self.ohm_checkbox.bind(active=self.on_checkbox_Active)

        # Add a label for each radio button.
        volt_label = Label(text="Volts\n(Electromotive force)",
                           halign='center',
                           font_size="10sp")
        self.radio_buttons_grid_layout.add_widget(volt_label)
        amp_label = Label(text="Amperes\n(Current)",
                          halign='center',
                          font_size="10sp")
        self.radio_buttons_grid_layout.add_widget(amp_label)
        ohm_label = Label(text="Ohms\n(Resistance)",
                          halign='center',
                          font_size="10sp")
        self.radio_buttons_grid_layout.add_widget(ohm_label)

        self.input_label = Label(text="2 - Enter the 2 required values:",
                                 pos_hint={"center_x": 0.5,
                                           "top": 0.6},
                                 size_hint=(0.9, 0.1))
        self.float_layout.add_widget(self.input_label)

        # Add a small grid layout for the V|I|R input fields.
        self.input_grid_layout = GridLayout(cols=3,
                                            rows=1,
                                            spacing=20,
                                            pos_hint={"center_x": 0.5,
                                                      "top": 0.5},
                                            size_hint=(0.9, 0.1))
        self.float_layout.add_widget(self.input_grid_layout)

        # Add number-input fields.
        self.volt_input = TextInput(font_size="25sp",
                                    input_type="number",
                                    input_filter="float",
                                    multiline=False,
                                    halign='center')
        self.input_grid_layout.add_widget(self.volt_input)

        self.amp_input = TextInput(font_size="25sp",
                                   input_type="number",
                                   input_filter="float",
                                   multiline=False,
                                   halign='center')
        self.input_grid_layout.add_widget(self.amp_input)

        self.ohm_input = TextInput(font_size="25sp",
                                   input_type="number",
                                   input_filter="float",
                                   multiline=False,
                                   halign='center')
        self.input_grid_layout.add_widget(self.ohm_input)

        # Add another grid layout for the buttons.
        self.buttons_grid_layout = GridLayout(cols=3,
                                              rows=1,
                                              spacing=20,
                                              pos_hint={"center_x": 0.5,
                                                        "top": 0.2},
                                              size_hint=(0.9, 0.1))
        self.float_layout.add_widget(self.buttons_grid_layout)

        # Add the instructions button.
        self.instructions_button = WhiteRoundedButton(text="Guide",
                                                      font_size="15sp")
        self.instructions_button.bind(on_press=self.show_instructions)
        self.buttons_grid_layout.add_widget(self.instructions_button)

        # Add the reset button.
        self.reset_button = ResetCalcButton(text="Reset",
                                            font_size="15sp")
        self.buttons_grid_layout.add_widget(self.reset_button)

        # Add a "Calculate" button.
        self.calculate_button = WhiteRoundedButton(text="Calculate",
                                                   font_size="15sp")
        self.calculate_button.bind(on_press=self.calculate_ohm_values)
        self.buttons_grid_layout.add_widget(self.calculate_button)

        # Once all the items are in place, activate one of the
        # radio buttons by default.
        self.volt_checkbox.state = "down"

    # Callback for the checkbox
    def on_checkbox_Active(self, checkboxInstance, isActive):
        """Deactivate the other two input fields and reset values."""
        if checkboxInstance.id == "volt_checkbox":
            self.amp_input.disabled = False
            self.ohm_input.disabled = False
            self.volt_input.disabled = True
        elif checkboxInstance.id == "amp_checkbox":
            self.amp_input.disabled = True
            self.ohm_input.disabled = False
            self.volt_input.disabled = False
        else:
            self.amp_input.disabled = False
            self.ohm_input.disabled = True
            self.volt_input.disabled = False
        # Reset the values in the input fields.
        for input_field in [self.amp_input, self.ohm_input, self.volt_input]:
            input_field.text = ""
        # Reset the values in the input fields.
        ResetButton._do_press(self)

    def calculate_ohm_values(self, instance):
        """Calculate values according to the currently selected option."""
        if self.amp_checkbox.active:
            if self.volt_input.text == "" or self.ohm_input.text == "":
                self.missing_values_warning()
            else:
                self.amp_input.text = str(round(float(self.volt_input.text) /
                                                float(self.ohm_input.text), 4))
        elif self.volt_checkbox.active:
            if self.amp_input.text == "" or self.ohm_input.text == "":
                self.missing_values_warning()
            else:
                self.volt_input.text = str(round(float(self.amp_input.text) *
                                                 float(self.ohm_input.text), 4))
        elif self.ohm_checkbox.active:
            if self.volt_input.text == "" or self.amp_input.text == "":
                self.missing_values_warning()
            else:
                self.ohm_input.text = str(round(float(self.volt_input.text) /
                                                float(self.amp_input.text), 4))

    def show_instructions(self, instance):
        """Display instructions for this section."""
        popup = OhmCalcInstructionsPopup()
        popup.open()

    def missing_values_warning(self):
        """Display a warning for missing values."""
        popup = OhmMissingValuesPopup()
        popup.open()


class OhmScreen(Screen):
    """
    Custom Screen Class for the Ohm's law simulator section.

    It inherits from Screen.
    """

    def __init__(self, **kwargs):
        """Class constructor."""
        super(OhmScreen, self).__init__(**kwargs)

        # Default value to be calculated.
        self.selected = "current"

        # Create a float layout.
        self.float_layout = FloatLayout()
        self.add_widget(self.float_layout)

        # Triangle image.
        self.triangle_image = Image(source="assets/images/I_318px-law_triangle.png",
                                    keep_ratio=False,
                                    size_hint=(None, None),
                                    width="150sp",
                                    height="150sp",
                                    allow_stretch=True,
                                    pos_hint={"center_x": 0.5, "top": 0.97})
        self.float_layout.add_widget(self.triangle_image)

        # Invisible grid layout and buttons for the triangle image.
        triangle_grid_layout = GridLayout(rows=2, cols=2,
                                          pos_hint={"center_x": 0.5,
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
                                      pos_hint={"center_x": 0.5, "bottom": 0},
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
        """Deactivate the slider corresponding to the selection option."""
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
        """Build and return the root widget."""
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
        self.screen_manager.add_widget(OhmCalcScreen(name="ohm_calc_screen"))
        self.screen_manager.add_widget(KirchhoffScreen(name="kirchhoff_screen"))
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
        """Bind the keyboard to listen to its behavior."""
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
        """Add our custom section to the default configuration object."""
        # We use the string defined above for our config JSON, but it could
        # also be loaded from a file as follows:
        #     settings.add_json_panel('My Label', self.config, 'settings.json')
        settings.add_json_panel('Configuración', self.config, data=CONFIG)

    def on_config_change(self, config, section, key, value):
        """Respond to changes in the configuration."""
        Logger.info("main.py: App.on_config_change: %s, %s, %s, %s,",
                    config, section, key, value)

        if section == "MenuScreenButton":
            if key == 'font_size':
                SettingsButton.font_size = float(value)

    def close_settings(self, settings=None):
        """Close the settings panel."""
        Logger.info("main.py: App.close_settings: %s", settings)
        super(Gilbert, self).close_settings(settings)


if __name__ == "__main__":
    Gilbert().run()
