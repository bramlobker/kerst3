import sys

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.uix.label import Label
from datetime import datetime
import random
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.dropdown import DropDown
import time
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle  # To draw the background color
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout


class SoundManagerApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.date = datetime.now().date()
        self.day = str(self.date).split("-")[2]
        self.start_button = Button(text="Start", font_size=50, background_color=(0.9, 0.2, 0.2, 1))
        self.stop_button = Button(text="Stop", font_size=50, background_color=(0.9, 0.2, 0.2, 1))
        self.option1 = Button(text='Kerkklokken Licht', size_hint_y=None, height=200, background_color=(0.9, 0.2, 0.2, 1),
                              font_size=50)
        self.option2 = Button(text='Kerkklokken Oldenzaal', size_hint_y=None, height=200,
                              background_color=(0.9, 0.2, 0.2, 1), font_size=50)
        self.option5 = Button(text='Kerkklokken Zwaar', size_hint_y=None, height=200,
                              background_color=(0.9, 0.2, 0.2, 1), font_size=50)
        self.option3 = Button(text='Carrillon Oh Denneboom', size_hint_y=None, height=200,
                              background_color=(0.9, 0.2, 0.2, 1), font_size=50)
        self.option4 = Button(text='Carrillon Oh Holy Night', size_hint_y=None, height=200,
                              background_color=(0.9, 0.2, 0.2, 1), font_size=50)

        self.option12 = Button(text='Midwinterhoorn', size_hint_y=None, height=200, background_color=(0.9, 0.2, 0.2, 1),
                               font_size=50)
        self.option22 = Button(text='Koortje', size_hint_y=None, height=200, background_color=(0.9, 0.2, 0.2, 1),
                               font_size=50)
        self.option32 = Button(text='Trein', size_hint_y=None, height=200, background_color=(0.9, 0.2, 0.2, 1),
                               font_size=50)
        self.option42 = Button(text='Paard', size_hint_y=None, height=200, background_color=(0.9, 0.2, 0.2, 1),
                               font_size=50)

        self.running = False  # Controls the main loop
        self.main_loop_event = None

        # Load sounds
        self.sounds = {
            "kb": SoundLoader.load("klok.mp3"),
            "kb2": SoundLoader.load("klok2.mp3"),
            "wind": SoundLoader.load("wind.mp3"),
            "talk": SoundLoader.load("talk.mp3"),
            "hoorn": SoundLoader.load("hoorn.mp3"),
            "hoorn2": SoundLoader.load("hoorn2.mp3"),
            "hoorn_vol": SoundLoader.load("hoorn_vol.mp3"),
            "koor": SoundLoader.load("koor.mp3"),
            "paard": SoundLoader.load("paard.wav"),
            "paard2": SoundLoader.load("paard2.mp3"),
            "car_tan": SoundLoader.load("c1.mp3"),
            "car_tan_vol": SoundLoader.load("c1_vol.mp3"),
            "car_ohn": SoundLoader.load("c2.mp3"),
            "car_ohn_vol": SoundLoader.load("c2_vol.mp3"),
            "trein": SoundLoader.load("trein.mp3"),
            "ambient": SoundLoader.load("ambient.mp3"),
            "ambient2": SoundLoader.load("ambient2.mp3"),
            "chatter": SoundLoader.load("chatter.mp3"),
            "chatter2": SoundLoader.load("chatter2.mp3"),
            "koor_vol": SoundLoader.load("koor_vol.mp3"),
            "beek": SoundLoader.load("beek.mp3"),
            "plenum_zwaar": SoundLoader.load("plenum_zwaar.mp3"),
            "plenum_licht": SoundLoader.load("plenum_licht.mp3"),
            "plenum_7klok": SoundLoader.load("plenum_7klokkig.mp3"),
            "fireworks": SoundLoader.load("fireworks.mp3"),
            "fireworks2": SoundLoader.load("fireworks2.mp3")
        }

        # Set volumes
        for key, sound in self.sounds.items():
            if sound:
                sound.volume = 0.3
            if key == "ambient":
                sound.volume = .6
            if key == "ambient2":
                sound.volume = .7
            if key == "beek":
                sound.volume = .15
            if key == "hoorn":
                sound.volume = .15
            if key == "hoorn2":
                sound.volume = .15
            if key == "hoorn_vol":
                sound.volume = .15
            if key == "talk":
                sound.volume = .1
            if key == "koor_vol":
                sound.volume = .3
            if key == "paard":
                sound.volume = .5
            if key == "paard2":
                sound.volume = .5
            if key == "trein":
                sound.volume = .1
            if key == "chatter":
                sound.volume = .04
            if key == "chatter2":
                sound.volume = .5
            if key == "plenum_zwaar":
                sound.volume = .6
            if key == "plenum_licht":
                sound.volume = .8
            if key == "plenum_7klok":
                sound.volume = .8
            if key == "kb":
                sound.volume = .8
            if key == "kb2":
                sound.volume = .8
            if key == "firework":
                sound.volume = .3
            if key == "fireworks2":
                sound.volume = .5

        # Randomized times
        self.paardTijd = sorted(random.sample(range(1, 60), 50))
        self.hoornTijd = self.generate_non_bunched_times(3, hour_minutes=60, min_gap=10)
        self.koorTijd = self.generate_non_bunched_times(3, hour_minutes=60, min_gap=10)
        self.fireworkTijd = self.generate_non_bunched_times(3, hour_minutes=60, min_gap=10)
        self.treinTijd = [9, 39]

    def build(self):

        # Set the resolution to Full HD
        Window.size = (1080, 1920)
        layout = BoxLayout(orientation="vertical")

        with layout.canvas.before:
            Color(0.1, 0.3, 0.1, 1)  # Dark Christmas green (RGB: 0, 99, 0)
            self.rect = Rectangle(size=layout.size, pos=layout.pos)
            layout.bind(size=self._update_rect, pos=self._update_rect)

        label = Label(text="NoelVille Geluidjes App", font_size=100, color=(169, 0, 0, 1))
        layout.add_widget(label)

        self.start_button.bind(on_press=self.start_sound_system)
        self.stop_button.bind(on_press=self.stop_sound_system)

        # Create the Dropdown menu for custom sound selection

        dropdown = DropDown()

        self.option1.bind(on_release=lambda btn: self.on_dropdown_select(btn))
        dropdown.add_widget(self.option1)
        self.option2.bind(on_release=lambda btn: self.on_dropdown_select(btn))
        dropdown.add_widget(self.option2)
        self.option3.bind(on_release=lambda btn: self.on_dropdown_select(btn))
        dropdown.add_widget(self.option3)
        self.option5.bind(on_release=lambda btn: self.on_dropdown_select(btn))
        dropdown.add_widget(self.option5)
        self.option4.bind(on_release=lambda btn: self.on_dropdown_select(btn))
        dropdown.add_widget(self.option4)

        # Main button that opens the dropdown
        dropdown_button = Button(text="Kies Kerkklokken", size_hint=(None, None), height=200, width=1080, font_size=50,
                                 background_color=(0.9, 0.2, 0.2, 1))
        dropdown_button.bind(on_release=dropdown.open)

        # DROPDOWN2
        dropdown2 = DropDown()

        self.option12.bind(on_release=lambda btn: self.on_dropdown_select(btn))
        dropdown2.add_widget(self.option12)
        self.option22.bind(on_release=lambda btn: self.on_dropdown_select(btn))
        dropdown2.add_widget(self.option22)
        self.option32.bind(on_release=lambda btn: self.on_dropdown_select(btn))
        dropdown2.add_widget(self.option32)
        self.option42.bind(on_release=lambda btn: self.on_dropdown_select(btn))
        dropdown2.add_widget(self.option42)

        # Main button that opens the dropdown
        dropdown_button2 = Button(text="Kies Geluid", size_hint=(None, None), height=200, width=1080, font_size=50,
                                  background_color=(0.9, 0.2, 0.2, 1))
        dropdown_button2.bind(on_release=dropdown2.open)

        layout.add_widget(self.start_button)
        layout.add_widget(self.stop_button)
        layout.add_widget(dropdown_button)
        layout.add_widget(dropdown_button2)

        return layout

    def on_dropdown_select(self, instance):
        # This callback is triggered when an item is selected from the dropdown
        print(f"Selected: {instance.text}")
        if instance.text == "Carrillon Oh Holy Night":
            if self.sounds["car_ohn_vol"].state == 'play':
                self.sounds["car_ohn_vol"].stop()
                self.option4.background_color = (0.9, 0.2, 0.2, 1)  # Change button color to green (RGBA)
            else:
                self.sounds["car_ohn_vol"].play()
                self.option4.background_color = (0, 1, 0, 1)  # Change button color to green (RGBA)

        if instance.text == "Carrillon Oh Denneboom":
            if self.sounds["car_tan_vol"].state == 'play':
                self.sounds["car_tan_vol"].stop()
                self.option3.background_color = (0.9, 0.2, 0.2, 1)  # Change button color to green (RGBA)
            else:
                self.sounds["car_tan_vol"].play()
                self.option3.background_color = (0, 1, 0, 1)  # Change button color to green (RGBA)

        if instance.text == "Kerkklokken Oldenzaal":
            if self.sounds["plenum_7klok"].state == 'play':
                self.sounds["plenum_7klok"].stop()
                self.option2.background_color = (0.9, 0.2, 0.2, 1)  # Change button color to green (RGBA)
            else:
                self.sounds["plenum_7klok"].play()
                self.option2.background_color = (0, 1, 0, 1)  # Change button color to green (RGBA)

        if instance.text == "Kerkklokken Licht":
            if self.sounds["plenum_licht"].state == 'play':
                self.sounds["plenum_licht"].stop()
                self.option1.background_color = (0.9, 0.2, 0.2, 1)  # Change button color to green (RGBA)
            else:
                self.sounds["plenum_licht"].play()
                self.option1.background_color = (0, 1, 0, 1)  # Change button color to green (RGBA)

        if instance.text == "Kerkklokken Zwaar":
            if self.sounds["plenum_zwaar"].state == 'play':
                self.sounds["plenum_zwaar"].stop()
                self.option5.background_color = (0.9, 0.2, 0.2, 1)  # Change button color to green (RGBA)
            else:
                self.sounds["plenum_zwaar"].play()
                self.option5.background_color = (0, 1, 0, 1)  # Change button color to green (RGBA)

        if instance.text == "Midwinterhoorn":
            if self.sounds["hoorn_vol"].state == 'play':
                self.sounds["hoorn_vol"].stop()
                self.option12.background_color = (0.9, 0.2, 0.2, 1)  # Change button color to green (RGBA)
            else:
                self.sounds["hoorn_vol"].play()
                self.option12.background_color = (0, 1, 0, 1)  # Change button color to green (RGBA)

        if instance.text == "Koortje":
            if self.sounds["koor_vol"].state == 'play':
                self.sounds["koor_vol"].stop()
                self.option22.background_color = (0.9, 0.2, 0.2, 1)  # Change button color to green (RGBA)
            else:
                self.sounds["koor_vol"].play()
                self.option22.background_color = (0, 1, 0, 1)  # Change button color to green (RGBA)

        if instance.text == "Trein":
            if self.sounds["trein"].state == 'play':
                self.sounds["trein"].stop()
                self.option32.background_color = (0.9, 0.2, 0.2, 1)  # Change button color to green (RGBA)
            else:
                self.sounds["trein"].play()
                self.option32.background_color = (0, 1, 0, 1)  # Change button color to green (RGBA)

        if instance.text == "Paard":
            if self.sounds["paard"].state == 'play':
                self.sounds["paard"].stop()
                self.option42.background_color = (0.9, 0.2, 0.2, 1)  # Change button color to green (RGBA)

            elif self.sounds["paard2"].state == 'play':
                self.sounds["paard2"].stop()
                self.option42.background_color = (0.9, 0.2, 0.2, 1)  # Change button color to green (RGBA)
            else:
                if random.choice([True, False]):
                    if self.sounds["paard"]:
                        self.sounds["paard"].play()
                        self.option42.background_color = (0, 1, 0, 1)  # Change button color to green (RGBA)
                else:
                    if self.sounds["paard2"]:
                        self.sounds["paard2"].play()
                        self.option42.background_color = (0, 1, 0, 1)  # Change button color to green (RGBA)

    def start_sound_system(self, instance):
        self.start_button.background_color = (0, 1, 0, 1)  # Change button color to green (RGBA)
        if not self.running:
            self.running = True
            self.playAmbient()
            self.main_loop_event = Clock.schedule_interval(self.main_loop, 1)  # Run every second

    def stop_sound_system(self, instance):
        if self.running:
            self.start_button.background_color = (0.9, 0.2, 0.2, 1)  # Change button color to green (RGBA)
            self.running = False
            Clock.unschedule(self.main_loop)

        for sound in self.sounds:
            self.sounds[sound].stop()

    def generate_non_bunched_times(self, num_times, hour_minutes=60, min_gap=5):
        times = []
        attempts = 0
        while len(times) < num_times and attempts < num_times * 10:
            new_time = random.randint(1, hour_minutes)
            if all(abs(new_time - t) >= min_gap for t in times):
                times.append(new_time)
            attempts += 1
        times.sort()
        return times

    def playPlenum(self, instance):
        if self.sounds["plenum_licht"]:
            self.sounds["plenum_licht"].play()

    def playPaard(self):
        if random.choice([True, False]):
            if self.sounds["paard"]:
                self.sounds["paard"].play()
        else:
            if self.sounds["paard2"]:
                self.sounds["paard2"].play()

    def playHoorn(self):
        if self.sounds["hoorn_vol"]:
            self.sounds["hoorn_vol"].play()

    def playAmbient(self):
        if self.sounds["ambient2"]:
            self.sounds["ambient2"].play()
        if self.sounds["beek"]:
            self.sounds["beek"].play()

        # Checks if day is 31st to play fireworks
        if str(self.date).split("-")[2] == "31":
            print("Firework")
            if self.sounds["fireworks"]:
                self.sounds["fireworks"].play()

    def playFirework(self):
        if str(self.date).split("-")[2] == "31":
            if self.sounds["fireworks2"]:
                self.sounds["fireworks2"].play()

    def check_minutes(self, times):
        minutes = times.minute
        if minutes in [15, 30, 45]:
            self.playAmbient()
            self.sounds["kb"].play()

        elif minutes in self.treinTijd:
            print("Trein")
            if self.sounds["trein"]:
                self.sounds["trein"].play()
        elif self.day == "31" and minutes in self.fireworkTijd:
            self.playFirework()
        elif minutes in self.hoornTijd:
            print("Midwinterhoorn")
            self.playHoorn()
        elif minutes in self.koorTijd:
            print("Koor")
            if self.sounds["koor_vol"]:
                self.sounds["koor_vol"].play()
        elif minutes in self.paardTijd:
            print("Paard")
            self.playPaard()

    def check_hour(self, times):
        minutes = times.minute
        if minutes == 0:
            # Reset times each hour
            self.paardTijd = sorted(random.sample(range(1, 60), 50))
            self.hoornTijd = self.generate_non_bunched_times(3, hour_minutes=60, min_gap=10)
            self.koorTijd = self.generate_non_bunched_times(3, hour_minutes=60, min_gap=10)
            print("Hourly reset: Paard:", self.paardTijd, "Hoorn:", self.hoornTijd, "Koor:", self.koorTijd)
            self.playAmbient()
            self.uurslag(times)

    def is_even(self, num):
        """Check if a number is even."""
        return num % 2 == 0

    def uurslag(self, times):

        # 12-hour format is used to simplify determining the number of rings, however...
        hour = times.hour if times.hour <= 12 else times.hour - 12  # 12-hour clock format
        # ... hour_real is needed for plenum on special birthdays on 12 at midnight, as simplified 12h clock format used cant differentiate between 12 noon and midnight
        hour_real = hour

        print(hour)
        if hour == 0:
            hour = 12

        i = 0
        # Alternate between kb and kb2 for each hour chime, playing the same files twice cuts off the first playback, which sounds weird
        while i < int(hour):
            if self.is_even(i):
                self.sounds["kb"].play()
            else:
                self.sounds["kb2"].play()
            time.sleep(3)  # Delay between chimes
            i += 1

        # Every Hour the short version of 'oh tannenbaum' is played, unless it's 12, 3, 6 or 9 hrs.
        if hour in [0, 3, 6, 9, 12]:

            # Play Church Bells for Dads Birthday
            if str(self.date) == "2025-12-24":
                # But only on midnight
                if hour_real == 0:
                    self.sounds["plenum_7klok"].play()
                else:
                    self.sounds["car_ohn_vol"].play()

            # Play Church Bells for Anne's Birthday
            elif str(self.date) == "2025-12-28":
                # But only on midnight
                if hour_real == 0:
                    self.sounds["plenum_licht"].play()
                else:
                    self.sounds["car_ohn_vol"].play()

            # Not a special day
            else:
                self.sounds["car_ohn_vol"].play()

        else:
            self.sounds["car_tan"].play()

    def updateDay(self):
        self.date = datetime.now().date()
        self.day = str(self.date).split("-")[2]

    def main_loop(self, dt):

        times = datetime.now()
        self.date = times.date()
        second = times.second
        if second == 0:
            self.updateDay()
            print("Checked Time:", times)
            self.check_minutes(times)
            self.check_hour(times)

    def _update_rect(self, *args):
        # Update the background rectangle when layout size or position changes
        self.rect.pos = self.root.pos
        self.rect.size = self.root.size


if __name__ == "__main__":
    SoundManagerApp().run()
