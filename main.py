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
from helper import *
from functools import partial


Builder.load_file('./UI/screen.kv')

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

    def message(self, activity, *largs):
        if activity == 'stretch':
            self.ids.lbl1.text = 'Time to stretch!\nActivate the exercise using the IMU.'
        if activity == 'breathe':
            self.ids.lbl1.text = 'Time to breathe!\nActivate the exercise using the IMU.'
        if activity == 'talk':
            self.ids.lbl1.text = 'Time to talk to friends!\nActivate sending a message using the IMU.'
        Clock.schedule_once(partial(self.activity_callback, activity, largs[0]))

    def message2(self, activity, time, *largs):
        if activity == 'stretch':
            self.ids.lbl1.text = 'Stretching activated! Follow Jackie\'s instructions :)'
        if activity == 'breathe':
            self.ids.lbl1.text = 'Follow along with the breathing exercise on the matrix!'
        if activity == 'talk':
            self.ids.lbl1.text = 'Say \'start recording\', wait 2 seconds, and record your message!\n (max: 10 seconds)'
        Clock.schedule_once(partial(self.exercise_callback, activity, time))

    def exercise_callback(self, activity, time, *largs):
        print('entered exercise callback')
        exercise(activity)
        if activity == 'talk':
            self.ids.lbl1.text = "Message saved and sending...\n\n" + congrats_message
        else:
            self.ids.lbl1.text = congrats_message
        congrats(activity)
        Clock.schedule_once(partial(self.message, activity), (time*60))  #gets called every hour

    def activity_callback(self, activity, time, *largs):
        print("entered callback for " + activity)
        activate(activity)
        Clock.schedule_once(partial(self.message2, activity, time))

    def on_pre_enter(self, *args):
        a = App.get_running_app()
        for k,v in a.big_dict.items():
            if v:
                Clock.schedule_once(partial(self.message, k), (a.time_dict[k] * 60))

class Root(ScreenManager):
    pass

class WAP(App):
    #which activities are necessary for day -- default is none
    big_dict=DictProperty({'stretch':False,'breathe':False,'talk':False})

    #time in minutes
    time_dict=DictProperty({'stretch':2,'breathe':.1,'talk':1})
    def build(self):
        return Root()

if __name__ == '__main__':
    WAP().run()
