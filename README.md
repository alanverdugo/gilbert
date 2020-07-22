# Gilbert

[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com)

Gilbert is an open source application written in [Python](https://www.python.org/) using [Kivy](https://kivy.org/#home). It was created by Alan Verdugo in order to help students learn about electricity and magnetism.

It was created with the [Autonomous University of Chihuahua (UACH)](https://uach.mx/) in mind, but hopefully this will help students all over the world.

Named after one of the great minds of science: [William Gilbert](https://en.wikipedia.org/wiki/William_Gilbert_(physician)), who made great contributions to the field of electromagnetism, among others.

---

## Usage
The application consist in different "sections". The main menu presents the available options. You can read the usage instructions for each section by using the "?" button in each screen, or by reading the following paragraphs.

### Study section
The study section is designed to provide a user-friendly way to study text lectures. Simply select the lecture in the upper-left menu and read on the right side panel.

### Quiz section
A student trying to test his or her knowledge will find this section useful. Random questions are presented in a quiz. The user selects the correct answers by pressing the appropiate button (which are also ordered randomly).

Counters indicating correct and incorrect questions are shown on the right side of the screen. Pressing the reset button on the lower right corner resets these counters.

### Ohm law simulator section
This section provides a simulation of how the Ohm law is calculated.
In the top of the screen, there is a triangle with the letters I (amperage), R (Resistance) and V (Voltage). Press any of them to calculate that value.

Once a value is selected the sliders for the two remaining values will become active. For example, if you choose to calculate V (Voltage), the sliders for I (Amperage) and R (Resistance) will activate.

Move the two sliders and see how the third value changes accordingly.

---

## Motivation

Gilbert was designed and built as completely free (libre) and open source software. I decided to do this for several reasons:

* I wanted the students to learn not just by using the application, but also by reading the code and understanding how it works.
* The users should be at ease knowing that they will never have to pay to use the application.
* The users should be at ease knowing that the application is not spying on them or using their data in malicious ways. They can be sure of this by inspecting the source code.
* If they want new features, the users can directly contribute to the proyect and help improve it for other people.

---

## Database

The application uses a SQLite database to store questions and answers in a very simple set of tables.

---

## Build

Since the application uses the Kivy framework, in order to build a valid APK file that could be installed in Android devices, a build process needs to happen.

The chosen tool for this is Buildozer. Read here for the Buildozer setup instructions: https://kivy.org/doc/stable/guide/packaging-android.html#buildozer

### Build a debug version of the application

First, connect your mobile device to the computer which will execute the build process.

```bash
buildozer android debug deploy run logcat > log.txt
```

If the build is successful, the application should be installed and start running in the connected Android device. Debug information should be written to the `log.txt` file in the current directory of the builder computer. This is extremelly useful to test the application on a real device.

### Build a release version of the application

```bash
buildozer android release
```

---

## How to contribute

Contributions to the project can be done in many ways. For example:

* Testing: Download and install the application in your device. Report any problems.
* Improve the code: Get an issue from the list and send a pull request with your changes.
* Spread the word: Tell other people about Gilbert.
* Donate: Help the open source proyects that helped Gilbert to become a reality. For example, you could donate to the [Python Software Foundation](https://www.python.org/psf/donations/), the [Kivy project](https://opencollective.com/kivy), the [Linux foundation](https://www.linuxfoundation.org/about/donate/) or the [Free Software Foundation](https://my.fsf.org/donate).

---

## License
Copyright 2020 Alan Verdugo Muñoz

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

[http://www.apache.org/licenses/LICENSE-2.0](http://www.apache.org/licenses/LICENSE-2.0)

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.