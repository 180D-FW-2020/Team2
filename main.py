import sys
import time
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.properties import DictProperty
from kivy.clock import Clock
from run.activate import activate

Builder.load_file('./UI/screen.kv')

#minutes
stretch_reminder = .1
breath_reminder = 1
talk_reminder = 1

congrats_message ="Congrats on completing a task!\nYou will be reminded to complete more tasks throughout the day."

class StartScreen(Screen):
    def __init__(self, **kw):
        super(StartScreen, self).__init__(**kw)
        self.a = App.get_running_app()
        self.e={}
    def ping(self,n, value):
        self.a.big_dict[n] = value
    def quit(self):
        sys.exit(0)

class WaitScreen(Screen):
    def __init__(self, **kw):
        super(WaitScreen, self).__init__(**kw)

    def stretch_callback(self, arg):
        print("entered callback")
        self.ids.lbl1.text = 'Time to stretch!\nActivate the exercise using the IMU.'
        activate('stretch')
        self.ids.lbl1.text = congrats_message
    def breath_callback(self, arg):
        print("entered callback")
        self.ids.lbl1.text = 'Time to breath!\nActivate the exercise using the IMU.'
        activate('breath')
        self.ids.lbl1.text = congrats_message
    def talk_callback(self, arg):
        print("entered callback")
        self.ids.lbl1.text = 'Time to talk to friends!\nActivate sending a message using the IMU.'
        activate('talk')
        self.ids.lbl1.text = congrats_message

    def on_pre_enter(self, *args):
        a = App.get_running_app()
        for k,v in a.big_dict.items():
            if v:
                if k == 'stretch':
                    Clock.schedule_interval(self.stretch_callback, stretch_reminder * 60)
                if k == 'breath':
                    Clock.schedule_interval(self.breath_callback, breath_reminder * 60)
                if k == 'talk':
                    Clock.schedule_interval(self.talk_callback, talk_reminder * 60)

class Root(ScreenManager):
    pass

class WAP(App):
    big_dict=DictProperty({'stretch':False,'breath':False,'talk':False})
    def build(self):
        return Root()

WAP().run()
