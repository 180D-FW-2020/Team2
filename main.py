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
from kivy.uix.textinput import TextInput
from kivy.uix.checkbox import CheckBox
from kivy.uix.boxlayout import BoxLayout

Builder.load_file('./UI/screen.kv')
TIME_INTERVAL = 30

class LoginScreen(Screen):
    def __init__(self, **kw):
        super(LoginScreen, self).__init__(**kw)

    def update(self):
        userID = self.ids.login.text
        if(userID !=''):
            id = open('ID.txt', 'w')
            id.write(userID)
            id.close()
            self.ids.login.background_color = (1, 1, 1, 1)
            self.manager.current = 'version'
            self.manager.transition.direction = 'left'
        else:
            self.ids.login.background_color = (1, 0, 0, .3)
            print('blank userID')
    def quit(self):
        sys.exit(0)

class VersionScreen(Screen):
    def __init__(self, **kw):
        super(VersionScreen, self).__init__(**kw)

    def ping(self, type):
        a = App.get_running_app()
        a.non_hardware = type

    def quit(self):
        sys.exit(0)

class StartScreen(Screen):
    def __init__(self, **kw):
        super(StartScreen, self).__init__(**kw)
        self.a = App.get_running_app()
        self.e={}
    def ping(self,n, value):
        self.a.big_dict[n][0] = value
    def quit(self):
        sys.exit(0)

class TimeScreen(Screen):
    def __init__(self, **kw):
        super(TimeScreen, self).__init__(**kw)

        self.widgets = {'stretch': [], 'breathe': [], 'talk': []}
        for k, v in self.widgets.items():
            self.make_selection(k)

    def ping(self, activity, time, *largs):
        a = App.get_running_app()
        a.big_dict[activity][1] = time

    def switch_back(self, *largs):
        a = App.get_running_app()
        for k,v in a.big_dict.items():
            if v[0]:
                self.ids.gl.remove_widget(self.widgets[k][0])
                self.ids.gl.remove_widget(self.widgets[k][1])
        self.manager.current = 'start'
        self.manager.transition.direction='right'
    def quit(self):
        sys.exit(0)

    def make_selection(self, k):
        if k == 'stretch':
            title = 'Stretching'
        if k == 'breathe':
            title = 'Breathing'
        if k == 'talk':
            title = "Talking to friends"

        ck30 = CheckBox(color=(0,0,0,1), group=k)
        ck30.bind(active=partial(self.ping, k, 30))
        ck60 = CheckBox(color=(0,0,0,1), group=k)
        ck60.bind(active=partial(self.ping, k, 60))
        ck90 = CheckBox(color=(0,0,0,1), group=k)
        ck90.bind(active=partial(self.ping, k, 90))

        lbl30 = Label(text='30 min', color=(0,0,0,1))
        lbl60 = Label(text='60 min', color=(0,0,0,1))
        lbl90 = Label(text='90 min', color=(0,0,0,1))
        lblblank = Label(text = '')

        time_gl = GridLayout(cols=2)

        time_gl.add_widget(ck30)
        time_gl.add_widget(lbl30)
        time_gl.add_widget(ck60)
        time_gl.add_widget(lbl60)
        time_gl.add_widget(ck90)
        time_gl.add_widget(lbl90)
        time_gl.add_widget(lblblank)

        box = BoxLayout(orientation='vertical',width=400,size_hint_x=None)
        box.add_widget(time_gl)

        text_label = Label(text=title, font_size=18, color=(0,0,0,1), width=200, size_hint_x=None)

        self.widgets[k].append(text_label)
        self.widgets[k].append(box)

    def on_pre_enter(self, *args):
        a = App.get_running_app()
        for k,v in a.big_dict.items():
            if v[0]:
                self.ids.gl.add_widget(self.widgets[k][0])
                self.ids.gl.add_widget(self.widgets[k][1])

class WaitScreen(Screen):
    def __init__(self, **kw):
        super(WaitScreen, self).__init__(**kw)

    def switch_screen(self, activity, *largs):
        self.manager.current = activity

    def switch_check(self, *largs):
        self.manager.current = 'check'

    def on_pre_enter(self, *args):
        a = App.get_running_app()
        print('entered wait')
        if a.immediate:
            Clock.schedule_once(self.switch_check)
        else:
            Clock.schedule_once(self.switch_check, TIME_INTERVAL) #*60) - a.time_elapsed)

class CheckScreen(Screen):
    def __init__(self, **kw):
        super(CheckScreen, self).__init__(**kw)

    def switch_screen(self, activity, *largs):
        self.manager.current = activity

    def switch_wait(self, *largs):
        self.manager.current = 'wait'

    def on_pre_enter(self, *args):
        a = App.get_running_app()

        activity = a.index
        act = a.big_dict[a.index]
        cur_time = a.cur_time

        print(activity)
        print(act)
        print(cur_time)

        if a.index == 'stretch':
            a.index = 'breathe'
            a.immediate = True
            a.time_elapsed = time.time()
        elif a.index == 'breathe':
            a.index = 'talk'
        elif a.index == 'talk':
            a.index = 'stretch'
            a.immediate = False
            a.cur_time += TIME_INTERVAL
            a.time_elapsed = time.time() - a.time_elapsed
        if act[0]:
            if cur_time % act[1]  == 0:
                Clock.schedule_once(partial(self.switch_screen, activity))
            else:
                print('skipping...')
                Clock.schedule_once(self.switch_wait)
        else:
            print('skipping...')
            Clock.schedule_once(self.switch_wait)

class TalkScreen(Screen):
    def __init__(self, **kw):
        super(TalkScreen, self).__init__(**kw)

    def switch(self, *largs):
        self.manager.current = 'talk2'

    def handle_input(self, *largs):
        a = App.get_running_app()
        a.dest_user = self.ids.txtinput.text
        Clock.schedule_once(self.switch)

    def get_user(self, *largs):
        self.ids.txtinput.bind(on_text_validate = self.handle_input)
        self.ids.lbl_talk.size_hint = (1, .7)
        self.ids.lbl_talk.text = 'Tell us which friend you want to send a message to!\nNote: must use their user ID.'
        self.ids.txtinput.size_hint = (1, .3)

    def on_enter(self, *args):
        if activate():
            Clock.schedule_once(self.get_user)
        else:
            a = App.get_running_app()
            a.index = 'stretch'
            a.immediate = 'False'
            a.cur_time += TIME_INTERVAL
            print('reminder snoozed')

class TalkScreen2(Screen):
    def __init__(self, **kw):
        super(TalkScreen2, self).__init__(**kw)

    def switch_congrats(self, *largs):
        self.manager.current = 'congrats'

    def activity(self, *largs):
        exercise_talk()
        Clock.schedule_once(self.switch_congrats)

    def on_enter(self, *args):
        a = App.get_running_app()
        Clock.schedule_once(self.activity, 1)

class StretchScreen(Screen):
    def __init__(self, **kw):
        super(StretchScreen, self).__init__(**kw)

    def switch_congrats(self, *largs):
        self.manager.current = 'congrats'

    def activity(self, *largs):
        exercise_stretch()
        Clock.schedule_once(self.switch_congrats)

    def on_enter(self, *args):
        if activate():
            self.ids.lbl_stretch.text = 'Stretching activated!\n\nYou have around 30 seconds to get your area ready.\nMake sure your entire body is in clear view of your webcam.'
            Clock.schedule_once(self.activity)
        else:
            print('reminder snoozed')
            a = App.get_running_app()
            a.index = 'stretch'
            a.immediate = 'False'
            a.cur_time += TIME_INTERVAL

class BreatheScreen(Screen):
    def __init__(self, **kw):
        super(BreatheScreen, self).__init__(**kw)

    def switch_congrats(self, *largs):
        self.manager.current = 'congrats'

    def activity(self, *largs):
        self.ids.lbl_breathe.text = 'Follow along with the breathing exercise on the matrix!'
        exercise_breathe()
        Clock.schedule_once(self.switch_congrats, 30)

    def on_enter(self, *args):
        if activate():
            Clock.schedule_once(self.activity)
        else:
            print('reminder snoozed')
            a = App.get_running_app()
            a.index = 'stretch'
            a.immediate = 'False'
            a.cur_time += TIME_INTERVAL

class CongratsScreen(Screen):
    def __init__(self, **kw):
        super(CongratsScreen, self).__init__(**kw)

    def switch_screen(self, *args):
        self.manager.current = 'wait'

    def on_enter(self, *args):
        congrats()
        Clock.schedule_once(self.switch_screen, 5)

class Root(ScreenManager):
    pass

class WAP(App):
    big_dict=DictProperty({'stretch':[False, 0],'breathe':[False, 0],'talk':[False,0]})

    #for iterating through dict at set intervals
    immediate = False
    index = 'stretch'
    cur_time = TIME_INTERVAL
    time_elapsed = 0

    dest_user = ''
    non_hardware = False

    def build(self):
        return Root()

if __name__ == '__main__':
    WAP().run()
