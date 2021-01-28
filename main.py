import sys
import time
from kivy.app import App
from kivy.app import Widget
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
from kivy.graphics import Color, Ellipse
from test_msg_sub import Listener
import threading
from playsound import playsound
import glob
import os

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

    def on_pre_enter(self):
        a = App.get_running_app()
        x = threading.Thread(target = a.listener.listen, daemon=True)
        x.start()

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
        self.time_check = time.time()
        self.time_check2 = time.time()
        self.lbl_normal=Label(text='Thank you for selecting your wellness actions!\nYou will be reminded to focus on these throughout the day.',halign='center',font_size=20,color=(0,0,0,1))

        self.btn_submit = Button(text='Activate', font_size=18, background_color=(.7,.7,1,1))
        self.btn_submit.bind(on_release=self.send_msg)
        self.btn_snooze = Button(text='Snooze', font_size=18, background_color=(.7,.7,1,1))
        self.btn_snooze.bind(on_release=self.update_screen2)
        self.gl = GridLayout(cols=2, height=125, size_hint_y=None)
        self.gl.add_widget(self.btn_snooze)
        self.gl.add_widget(self.btn_submit)

    def switch_check(self, *largs):
        self.manager.current = 'check'

    def switch_congrats(self, *largs):
        Clock.unschedule(self.check_congrats)
        self.manager.current = 'congrats'

    def update_screen2(self, *args):
        try:
            self.ids.boxy.remove_widget(self.lbl)
            self.ids.boxy.remove_widget(self.lbl1)
            self.ids.boxy.remove_widget(self.lbl2)
            self.ids.boxy.remove_widget(self.lbl3)
            self.ids.boxy.remove_widget(self.gl)
        except:
            print('widgets already removed')
        self.ids.boxy.add_widget(self.lbl_normal)

    def update_screen(self,*args):
        latest_audio = max(glob.iglob('./RecAudio/*'), key=os.path.getctime)
        playsound(latest_audio)
        try:
            self.ids.boxy.remove_widget(self.lbl)
            self.ids.boxy.remove_widget(self.lbl1)
            self.ids.boxy.remove_widget(self.lbl2)
            self.ids.boxy.remove_widget(self.lbl3)
            self.ids.boxy.remove_widget(self.gl)
        except:
            print('widgets already removed')
        self.ids.boxy.add_widget(self.lbl_normal)

    def send_msg(self, *largs):
        a = App.get_running_app()
        try:
            self.ids.boxy.remove_widget(self.lbl)
            self.ids.boxy.remove_widget(self.lbl1)
            self.ids.boxy.remove_widget(self.lbl2)
            self.ids.boxy.remove_widget(self.lbl3)
        except:
            print('end me.')
        msg = 'Say \'start recording\', wait 2 seconds, and record your message!\n (max: 10 seconds)'
        self.lbl3 = Label(text=msg,halign='center',font_size=20,color=(0,0,0,1))
        self.ids.boxy.remove_widget(self.lbl_normal)
        self.ids.boxy.add_widget(self.lbl3)
        exercise_talk(a.listener.dest_user)
        Clock.schedule_once(self.update_screen2)

    def check_other(self, *largs):
        a = App.get_running_app()
        if a.listener.congrats and (time.time() > (self.time_check2 + 10)):
            self.time_check2 = time.time()
            self.ids.boxy.remove_widget(self.lbl_normal)
            print('SOMEBODY FINISHED SMTHG WOWOWOWOW')
            if a.non_hardware:
                print('dear god end my pain')
                msg = 'Your friend ' + a.listener.dest_user + ' just completed a task!\n Activate using the buttons if you want to send a message to them.'
                self.lbl2 = Label(text=msg,halign='center',font_size=20,color=(0,0,0,1))
                self.ids.boxy.add_widget(self.lbl2)
                self.ids.boxy.add_widget(self.gl)
            else:
                msg = 'Your friend ' + a.listener.dest_user + ' just completed a task!\n Activate using the IMU if you want to send a message to them.'
                self.lbl1 = Label(text=msg,halign='center',font_size=20,color=(0,0,0,1))
                self.ids.boxy.add_widget(self.lbl1)

                a.listener.set_activated(False)
                t_now = time.time()
                while time.time() < (t_now +2*60):
                    if a.listener.activated:
                        break
                    if a.listener.snoozed:
                        break
                print(a.listener.activated)
                if a.listener.activated:
                    Clock.schedule_once(self.send_msg)
                else:
                    Clock.schedule_once(self.snooze)

    def check_congrats(self, *largs):
        a = App.get_running_app()
        if a.listener.received and (time.time() > (self.time_check + 10)):
            self.time_check = time.time()
            print('RECEIVED MSG')
            latest_txt = max(glob.iglob('./RecTxt/*'), key=os.path.getctime)
            f = open(latest_txt)
            msg = f.readline()
            display_msg = 'Your friend said:\n' + msg
            print(display_msg)
            self.lbl = Label(text=display_msg,halign='center',font_size=20,color=(0,0,0,1))
            self.ids.boxy.remove_widget(self.lbl_normal)
            self.ids.boxy.add_widget(self.lbl)
            Clock.schedule_once(self.update_screen)

    def on_pre_enter(self, *args):
        a = App.get_running_app()
        print('entered wait')
        try:
            self.ids.boxy.add_widget(self.lbl_normal)
        except:
            print('already added')
        if a.immediate:
            Clock.schedule_once(self.switch_check)
        else:
            if a.completed:
                Clock.schedule_once(self.switch_congrats)
                a.completed = False
            else:
                Clock.schedule_interval(self.check_congrats, 1)
                Clock.schedule_interval(self.check_other, 1)
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
        print(a.completed)

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
        self.btn_submit = Button(text='Activate', font_size=18, background_color=(.7,.7,1,1))
        self.btn_submit.bind(on_release=self.get_user)
        self.btn_snooze = Button(text='Snooze', font_size=18, background_color=(.7,.7,1,1))
        self.btn_snooze.bind(on_release=self.snooze)
        self.gl = GridLayout(cols=2, height=125, size_hint_y=None)
        self.gl.add_widget(self.btn_snooze)
        self.gl.add_widget(self.btn_submit)

    def switch(self, *largs):
        self.manager.current = 'talk2'

    def handle_input(self, *largs):
        a = App.get_running_app()
        a.dest_user = self.ids.txtinput.text
        Clock.schedule_once(self.switch)

    def get_user(self, *largs):
        self.ids.bl_talk.remove_widget(self.gl)
        self.ids.txtinput.bind(on_text_validate = self.handle_input)
        self.ids.lbl_talk.size_hint = (1, .7)
        self.ids.lbl_talk.text = 'Tell us which friend you want to send a message to!\nNote: must use their user ID.'
        self.ids.txtinput.size_hint = (1, .3)

    def snooze(self, *args):
        self.ids.bl_talk.remove_widget(self.gl)
        a = App.get_running_app()
        a.index = 'stretch'
        a.immediate = False
        a.cur_time += TIME_INTERVAL
        self.manager.current = 'wait'
        print('reminder snoozed')

    def on_pre_enter(self, *args):
        a = App.get_running_app()
        if a.non_hardware:
            self.ids.lbl_talk.text='Time to talk to friends!\nActivate sending a message using the buttons below.'
            self.ids.bl_talk.add_widget(self.gl)
        else:
            activate()
            a.listener.set_activated(False)
            t_now = time.time()
            while time.time() < (t_now +2*60):
                if a.listener.activated:
                    break
                if a.listener.snoozed:
                    break
            print(a.listener.activated)
            if a.listener.activated:
                Clock.schedule_once(self.get_user)
            else:
                Clock.schedule_once(self.snooze)

class TalkScreen2(Screen):
    def __init__(self, **kw):
        super(TalkScreen2, self).__init__(**kw)

    def switch_congrats(self, *largs):
        a = App.get_running_app()
        a.completed = True
        self.manager.current = 'wait'

    def activity(self, *largs):
        a = App.get_running_app()
        exercise_talk(a.dest_user)
        Clock.schedule_once(self.switch_congrats)

    def on_enter(self, *args):
        a = App.get_running_app()
        Clock.schedule_once(self.activity, 1)

class StretchScreen(Screen):
    def __init__(self, **kw):
        super(StretchScreen, self).__init__(**kw)
        self.btn_submit = Button(text='Activate', font_size=18, background_color=(.7,.7,1,1))
        self.btn_submit.bind(on_release=self.transition)
        self.btn_snooze = Button(text='Snooze', font_size=18, background_color=(.7,.7,1,1))
        self.btn_snooze.bind(on_release=self.snooze)
        self.gl = GridLayout(cols=2, height=125, size_hint_y=None)
        self.gl.add_widget(self.btn_snooze)
        self.gl.add_widget(self.btn_submit)

    def switch_congrats(self, *largs):
        a = App.get_running_app()
        a.completed = True
        self.manager.current = 'wait'

    def activity(self, *largs):
        exercise_stretch()
        Clock.schedule_once(self.switch_congrats)

    def snooze(self, *args):
        self.ids.bl_stretch.remove_widget(self.gl)
        a = App.get_running_app()
        a.index = 'stretch'
        a.immediate = False
        a.cur_time += TIME_INTERVAL
        self.manager.current = 'wait'
        print('reminder snoozed')

    def transition(self, *args):
        self.ids.bl_stretch.remove_widget(self.gl)
        self.ids.lbl_stretch.text = 'Stretching activated!\n\nYou have around 30 seconds to get your area ready.\nMake sure your entire body is in clear view of your webcam.'
        Clock.schedule_once(self.activity)

    def on_pre_enter(self, *args):
        a = App.get_running_app()
        if a.non_hardware:
            self.ids.lbl_stretch.text='Time to stretch!\nActivate using the buttons below.'
            self.ids.bl_stretch.add_widget(self.gl)
        else:
            activate()
            a.listener.set_activated(False)
            t_now = time.time()
            while time.time() < (t_now +2*60):
                if a.listener.activated:
                    break
                if a.listener.snoozed:
                    break
            print(a.listener.activated)
            if a.listener.activated:
                Clock.schedule_once(self.activity)
            else:
                Clock.schedule_once(self.snooze)

class BreatheScreen(Screen):
    def __init__(self, **kw):
        super(BreatheScreen, self).__init__(**kw)
        self.btn_submit = Button(text='Activate', font_size=18, background_color=(.7,.7,1,1))
        self.btn_submit.bind(on_release=self.activity_software)
        self.btn_snooze = Button(text='Snooze', font_size=18, background_color=(.7,.7,1,1))
        self.btn_snooze.bind(on_release=self.snooze)
        self.gl = GridLayout(cols=2, height=125, size_hint_y=None)
        self.gl.add_widget(self.btn_snooze)
        self.gl.add_widget(self.btn_submit)

    def switch_congrats(self, *largs):
        a = App.get_running_app()
        a.completed = True
        self.manager.current = 'wait'

    def snooze(self, *args):
        self.ids.bl_breathe.remove_widget(self.gl)
        a = App.get_running_app()
        a.index = 'stretch'
        a.immediate = False
        a.cur_time += TIME_INTERVAL
        self.manager.current = 'wait'
        print('reminder snoozed')

    def activity_software2 (self, dt):
        self.manager.current = 'ball'

    def activity_software(self, *largs):
        self.ids.bl_breathe.remove_widget(self.gl)
        self.ids.lbl_breathe.text = 'Breathe with the ball on the screen.'
        Clock.schedule_once(self.activity_software2, 3.5)

    def activity(self, *largs):
        self.ids.lbl_breathe.text = 'Follow along with the breathing exercise on the matrix!'
        exercise_breathe()
        Clock.schedule_once(self.switch_congrats, 30)

    def on_pre_enter(self, *args):
        a = App.get_running_app()
        if a.non_hardware:
            self.ids.lbl_breathe.text='Time to breathe!\nActivate using the buttons below.'
            self.ids.bl_breathe.add_widget(self.gl)
        else:
            activate()
            a.listener.set_activated(False)
            t_now = time.time()
            while time.time() < (t_now +2*60):
                if a.listener.activated:
                    break
                if a.listener.snoozed:
                    break
            print(a.listener.activated)
            if a.listener.activated:
                Clock.schedule_once(self.activity)
            else:
                Clock.schedule_once(self.snooze)

class BallScreen(Screen):
    def __init__(self, **kw):
        super(BallScreen, self).__init__(**kw)
        self.size_ball_x = 101
        self.size_ball_y = 101
        self.inc = True

    def switch_congrats(self, *largs):
        a = App.get_running_app()
        self.canvas.clear()
        Clock.unschedule(self.ball)
        a.completed = True
        self.manager.current = 'wait'

    def ball(self, dt):
        self.canvas.clear()
        with self.canvas:
            Color(.7,.7,1,1)
            Ellipse(pos= (self.center_x - (self.size_ball_x/2), self.center_y - (self.size_ball_y/2)), size=(self.size_ball_x,self.size_ball_y))
        if self.size_ball_x == 200 or self.size_ball_x == 100:
            self.inc = not self.inc
        if self.inc:
            self.size_ball_x += 1
            self.size_ball_y += 1
        else:
            self.size_ball_x -= 1
            self.size_ball_y -= 1

    def on_enter(self):
        Clock.schedule_interval(self.ball, .05)
        Clock.schedule_once(self.switch_congrats, 30)

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
    completed = False
    index = 'stretch'
    cur_time = TIME_INTERVAL
    time_elapsed = 0

    dest_user = ''
    non_hardware = False

    listener = Listener()

    def build(self):
        return Root()

if __name__ == '__main__':
    WAP().run()
