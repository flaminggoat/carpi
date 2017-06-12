#!/usr/bin/python3
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder

import time

#Builder.load_file("car.kv")

class RootWidget(Widget):
    def __init__(self, **kwargs):
        super(RootWidget, self).__init__(**kwargs)
        Clock.schedule_interval(self.update, 1.0/60.0)
    def update(self, dt):
        clock = self.ids.clock
        clock.text = time.strftime('%I:%M %d/%m/%Y',time.localtime())
    def setScreen(self, newScreen):
        self.ids.screen_manager.current = newScreen

class MusicScreen(Screen):
    pass

class MenuScreen(Screen):
    pass

class CarApp(App):
    def build(self):
        self.root = RootWidget()
        #Clock.schedule_interval(m.update, 1.0/60.0)
        #sm.current = 'music'
        return self.root
   
if __name__ == '__main__':
    CarApp().run()
