#!/usr/bin/python3
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen

import time

#Create screen manager
sm = ScreenManager()

class MainScreen(Screen):
    def update(self, dt):
        clock = self.ids.clock
        clock.text = time.strftime('%I:%M %d/%m/%Y',time.localtime())

class MusicScreen(Screen):
    pass

class CarApp(App):
    def build(self):
        m = MainScreen()
        Clock.schedule_interval(m.update, 1.0/60.0)
        return m
    
if __name__ == '__main__':
    CarApp().run()
