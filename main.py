import sys
import time
from kivy.app import App
from kivy.app import Widget
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition, SlideTransition
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
from MQTT.pub import PUB
from Speech.audio_msg import speech
from rpi_conn import rpi_conn

Builder.load_file('./UI/screen.kv')
TIME_INTERVAL = 30
debug = 1


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
        self.a = App.get_running_app()

    def ping(self, type):
        self.a.non_hardware = type

    def switch(self):
        self.manager.transition.direction='left'
        if self.a.non_hardware:
            self.manager.current='start'
        else:
            self.manager.current='raspberry'

    def quit(self):
        sys.exit(0)

class RaspberryScreen(Screen):
    def __init__(self, **kw):
        super(RaspberryScreen, self).__init__(**kw)
        self.a=App.get_running_app()

    def connect(self, *args):
        if not self.t1.isAlive():
            Clock.unschedule(self.connect)
            if self.a.rpi_conn.connected:
                self.manager.current = 'start'
                self.manager.transition.direction='left'
            else:
                self.ids.lbl.text = 'Error connecting. Please verify your login information is correct.'
                self.ids.ip.background_color = (1, 0, 0, .3)
                self.ids.port.background_color = (1, 0, 0, .3)
                self.ids.user.background_color = (1, 0, 0, .3)
                self.ids.pw.background_color = (1, 0, 0, .3)

    def update(self):
        self.ids.lbl.text='connecting...'
        self.ip = self.ids.ip.text
        self.port = self.ids.port.text
        self.user = self.ids.user.text
        self.pw = self.ids.pw.text
        if self.ip == '' or self.port == '' or self.user == '' or self.pw == '':
            if self.ip =='':
                self.ids.ip.background_color = (1, 0, 0, .3)
            if self.port == '':
                self.ids.port.background_color = (1, 0, 0, .3)
            if self.user == '':
                self.ids.user.background_color = (1, 0, 0, .3)
            if self.pw == '':
                self.ids.pw.background_color = (1, 0, 0, .3)
        else:
            f = open('rpi.txt', 'w')
            new_info = 'ip=' + self.ip + '\n' + 'port=' + self.port
            f.write(new_info)
            f.close()
            self.a.rpi_conn.set_conn_info(str(self.ip), int(self.port), str(self.user), str(self.pw))
            self.t1 = threading.Thread(target=self.a.rpi_conn.connect, daemon=True)
            self.t1.start()
            Clock.schedule_interval(self.connect, .1)

    def on_pre_enter(self):
        f = open('rpi.txt', 'r')
        self.ids.ip.text = f.readline().split('=')[1].replace('\n', '')
        self.ids.port.text = f.readline().split('=')[1].replace('\n', '')
        f.close()

    def on_leave(self):
        self.ids.lbl.text = 'Enter your Raspberry Pi connection information below.'
        self.ids.ip.background_color = (1, 1, 1, 1)
        self.ids.port.background_color = (1, 1, 1, 1)
        self.ids.user.background_color = (1, 1, 1, 1)
        self.ids.pw.background_color = (1, 1, 1, 1)

    def quit(self):
        sys.exit(0)

class StartScreen(Screen):
    def __init__(self, **kw):
        super(StartScreen, self).__init__(**kw)
        self.a = App.get_running_app()
        self.e={}

    def ping(self,n, value):
        self.a.big_dict[n][0] = value

    def switch(self):
        self.manager.transition.direction='right'
        if self.a.non_hardware:
            self.manager.current='version'
        else:
            self.manager.current='raspberry'

    def quit(self):
        sys.exit(0)

class TimeScreen(Screen):
    def __init__(self, **kw):
        super(TimeScreen, self).__init__(**kw)
        self.a = App.get_running_app()
        self.widgets = {'stretch': [], 'breathe': [], 'talk': []}
        for k, v in self.widgets.items():
            self.make_selection(k)

    def ping(self, activity, time, *args):
        self.a.big_dict[activity][1] = time

    def switch_back(self, *args):
        for k,v in self.a.big_dict.items():
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

        box = BoxLayout(orientation='vertical')
        box.add_widget(time_gl)

        text_label = Label(text=title, font_size=18, color=(0,0,0,1))

        self.widgets[k].append(text_label)
        self.widgets[k].append(box)

    def on_pre_enter(self, *args):
        for k,v in self.a.big_dict.items():
            if v[0]:
                self.ids.gl.add_widget(self.widgets[k][0])
                self.ids.gl.add_widget(self.widgets[k][1])

class WaitScreen(Screen):
    def __init__(self, **kw):
        super(WaitScreen, self).__init__(**kw)
        self.time_check_msg = time.time()
        self.time_check_congrats = time.time()
        self.lbl_normal=Label(text='Thank you for selecting your wellness actions!\nYou will be reminded to focus on these throughout the day.',halign='center',font_size=20,color=(0,0,0,1))
        self.a = App.get_running_app()
        self.make_activation_widget()
        self.make_recording_labels()

    def make_recording_labels(self):
        self.lbl_speak = Label(text='Say \'start recording\' to send a message!',halign='center',font_size=20,color=(0,0,0,1))
        self.lbl_start_recog=Label(text='Start command recognized, get ready to send your message :)',halign='center',font_size=20,color=(0,0,0,1))
        self.lbl_start_not_recog=Label(text='Start command not recognized, please try again.',halign='center',font_size=20,color=(0,0,0,1))
        self.lbl_recording = Label(text='Send over an audio message! (Max: 10 seconds)',halign='center',font_size=20,color=(0,0,0,1))
        self.lbl_save=Label(text='Saving message transcription...',halign='center',font_size=20,color=(0,0,0,1))
        self.lbl_send = Label(text='Sending message...',halign='center',font_size=20,color=(0,0,0,1))

    def make_activation_widget(self):
        self.btn_submit = Button(text='Activate', font_size=18, background_color=(.7,.7,1,1))
        self.btn_submit.bind(on_release=self.start_msg)
        self.btn_snooze = Button(text='Snooze', font_size=18, background_color=(.7,.7,1,1))
        self.btn_snooze.bind(on_release=self.update_screen_snooze)
        self.gl = GridLayout(cols=2, height=125, size_hint_y=None)
        self.gl.add_widget(self.btn_snooze)
        self.gl.add_widget(self.btn_submit)

    def on_leave(self):
        Clock.unschedule(self.check_for_messages)
        Clock.unschedule(self.check_others_finished)

    def switch_check(self, *args):
        self.manager.current = 'check'

    def switch_congrats(self, *args):
        self.manager.current = 'congrats'

    def update_screen_snooze(self, *args):
        if self.a.non_hardware:
            self.ids.boxy.remove_widget(self.lbl_friend_finished)
            self.ids.boxy.remove_widget(self.gl)
        else:
            self.ids.boxy.remove_widget(self.lbl_friend_finished_hardware)
        self.ids.boxy.add_widget(self.lbl_normal)

    def update_screen_completed(self, *args):
        self.ids.boxy.remove_widget(self.lbl_send)
        self.ids.boxy.add_widget(self.lbl_normal)

    def wait_for_activate(self, *args):
        self.a.listener.set_activated(False)
        t_now = time.time()
        while time.time() < (t_now +2*60):
            if self.a.listener.activated:
                break
            if self.a.listener.snoozed:
                break

    def check_hardware_activate(self, *args):
        if not self.t1.isAlive():
            Clock.unschedule(self.check_hardware_activate)
            if self.a.listener.activated:
                Clock.schedule_once(self.start_msg)
            else:
                Clock.schedule_once(self.update_screen_snooze)

    def send_msg(self, *args):
        audio_topic = '/' + self.a.listener.dest_user + '/audio'
        txt_topic = '/' + self.a.listener.dest_user + '/text'
        audio_path = self.a.speech_instance.get_audiopath()
        txt_path = self.a.speech_instance.get_txtpath()
        pub = PUB(audio_topic, "hello from audio")
        client = pub.connect_mqtt()
        client.loop_start()
        pub.publish_file(client, audio_path)
        client.disconnect()

        pub = PUB(txt_topic, self.a.listener.dest_user + 'hello from txt')
        client = pub.connect_mqtt()
        client.loop_start()
        pub.publish_file(client, txt_path)
        client.disconnect()
        Clock.schedule_once(self.update_screen_completed)

    def trans_send(self, *args):
        self.ids.boxy.remove_widget(self.lbl_save)
        self.ids.boxy.add_widget(self.lbl_send)
        Clock.schedule_once(self.send_msg)

    def transcribe_msg(self, *args):
        self.ids.boxy.remove_widget(self.lbl_recording)
        self.ids.boxy.add_widget(self.lbl_save)
        self.a.speech_instance.transcribe()
        Clock.schedule_once(self.trans_send)

    def record_msg(self, *args):
        print('recording...')
        self.a.speech_instance.record_msg()
        Clock.schedule_once(self.transcribe_msg)

    def cor_rec(self, *args):
        self.ids.boxy.remove_widget(self.lbl_start_recog)
        self.ids.boxy.add_widget(self.lbl_recording)
        Clock.schedule_once(self.record_msg)

    def correct(self, *args):
        print("Start command recognized!")
        try:
            self.ids.boxy.remove_widget(self.lbl_start_not_recog)
        except:
            print('got it first try gj')
        self.ids.boxy.remove_widget(self.lbl_speak)
        self.ids.boxy.add_widget(self.lbl_start_recog)
        Clock.schedule_once(self.cor_rec, 2)

    def not_correct(self, *args):
        self.ids.boxy.remove_widget(self.lbl_speak)
        self.ids.boxy.add_widget(self.lbl_speech)
        try:
            self.ids.boxy.add_widget(self.lbl_start_not_recog)
        except:
            print('you already messed up once my dude')
        print("Start command not recognized...")
        Clock.schedule_once(self.recognize_start, .1)

    def recognize_start(self, *args):
        for j in range(1):
            print('Speak!')
            time.sleep(0.5)
            guess = self.a.speech_instance.recognize_speech_from_mic()
            if guess["transcription"]:
                break
            if not guess["success"]:
                break
            print("I didn't catch that. What did you say?\n")
            if guess["error"]:
                print("ERROR: {}".format(guess["error"]))
                break
        try:
            self.ids.boxy.remove_widget(self.lbl_speech)
            self.ids.boxy.add_widget(self.lbl_speak)
        except:
            print('first run')

        msg = "You said: {}".format(guess["transcription"])
        self.lbl_speech = Label(text=msg,halign='center',font_size=20,color=(0,0,0,1))
        print(msg)

        if str(guess["transcription"]).find("start recording") != -1:
            Clock.schedule_once(self.correct)
        else:
            Clock.schedule_once(self.not_correct)

    def start_msg(self, *args):
        if self.a.non_hardware:
            self.ids.boxy.remove_widget(self.lbl_friend_finished)
            self.ids.boxy.remove_widget(self.gl)
        else:
            self.ids.boxy.remove_widget(self.lbl_friend_finished_hardware)
        self.ids.boxy.add_widget(self.lbl_speak)
        Clock.schedule_once(self.recognize_start, .1)

    def check_others_finished(self, *args):
        if self.a.listener.congrats and (time.time() > (self.time_check_congrats + 10)):
            self.time_check_congrats = time.time()
            self.ids.boxy.remove_widget(self.lbl_normal)
            print('SOMEBODY FINISHED SMTHG WOWOWOWOW')
            if self.a.non_hardware:
                print('entered non hardware')
                try:
                    self.ids.boxy.remove_widget(self.lbl_friend_finished)
                except:
                    pass
                msg = 'Your friend ' + self.a.listener.dest_user + ' just completed a task!\n Activate using the buttons if you want to send a message to them.'
                self.lbl_friend_finished = Label(text=msg,halign='center',font_size=20,color=(0,0,0,1))
                self.ids.boxy.add_widget(self.lbl_friend_finished)
                try:
                    self.ids.boxy.add_widget(self.gl)
                except:
                    pass
            else:
                print('entered hardware')
                msg = 'Your friend ' + self.a.listener.dest_user + ' just completed a task!\n Activate using the IMU if you want to send a message to them.'
                self.lbl_friend_finished_hardware = Label(text=msg,halign='center',font_size=20,color=(0,0,0,1))
                self.ids.boxy.add_widget(self.lbl_friend_finished_hardware)
                self.t1 = threading.Thread(target=self.wait_for_activate, daemon=True)
                self.t1.start()
                Clock.schedule_interval(self.check_hardware_activate, .1)

    def update_screen(self,*args):
        try:
            latest_audio = max(glob.iglob('./RecAudio/*'), key=os.path.getctime)
            playsound(latest_audio)
        except:
            print('error: audio could not play')
        self.ids.boxy.remove_widget(self.lbl_msg)
        self.ids.boxy.add_widget(self.lbl_normal)

    def check_for_messages(self, *args):
        if self.a.listener.received and not self.a.listener.sent_from_me and (time.time() > (self.time_check_msg + 10)):
            self.time_check_msg = time.time()
            print('RECEIVED MSG')
            latest_txt = max(glob.iglob('./RecTxt/*'), key=os.path.getctime)
            f = open(latest_txt)
            msg = f.readline()
            display_msg = 'Your friend said:\n' + msg
            print(display_msg)
            self.lbl_msg = Label(text=display_msg,halign='center',font_size=20,color=(0,0,0,1))
            self.ids.boxy.remove_widget(self.lbl_normal)
            self.ids.boxy.add_widget(self.lbl_msg)
            Clock.schedule_once(self.update_screen)

    def on_pre_enter(self, *args):
        print('entered wait')

        try:
            self.ids.boxy.add_widget(self.lbl_normal)
        except:
            pass

        if self.a.first_run:
            self.a.first_run = False
            x = threading.Thread(target = self.a.listener.listen, daemon=True)
            x.start()
            if not self.a.non_hardware:
                y = threading.Thread(target = self.a.rpi_conn.run, daemon=True)
                y.start()

        if self.a.immediate:
            Clock.schedule_once(self.switch_check)
        else:
            if self.a.completed:
                Clock.schedule_once(self.switch_congrats)
                self.a.completed = False
            else:
                Clock.schedule_interval(self.check_for_messages, 1)
                Clock.schedule_interval(self.check_others_finished, 1)
                if debug:
                    Clock.schedule_once(self.switch_check, TIME_INTERVAL)
                else:
                    Clock.schedule_once(self.switch_check, TIME_INTERVAL*60 - self.a.time_elapsed)

class CheckScreen(Screen):
    def __init__(self, **kw):
        super(CheckScreen, self).__init__(**kw)
        self.a = App.get_running_app()

    def switch_screen(self, activity, *largs):
        self.manager.current = activity

    def switch_wait(self, *largs):
        self.manager.current = 'wait'

    def on_pre_enter(self, *args):
        activity = self.a.index
        act = self.a.big_dict[self.a.index]
        cur_time = self.a.cur_time

        if self.a.index == 'stretch':
            self.a.index = 'breathe'
            self.a.immediate = True
            self.a.time_elapsed = time.time()
        elif self.a.index == 'breathe':
            self.a.index = 'talk'
        elif self.a.index == 'talk':
            self.a.index = 'stretch'
            self.a.immediate = False
            self.a.cur_time += TIME_INTERVAL
            self.a.time_elapsed = time.time() - self.a.time_elapsed
        if act[0]:
            if cur_time % act[1]  == 0:
                Clock.schedule_once(partial(self.switch_screen, activity))
            else:
                Clock.schedule_once(self.switch_wait)
        else:
            Clock.schedule_once(self.switch_wait)

class TalkScreen(Screen):
    def __init__(self, **kw):
        super(TalkScreen, self).__init__(**kw)
        self.txtinput=TextInput(hint_text='Press enter to submit.\n\nMust use their user ID. If you wish to send to everyone on the network, enter \'all\'.', multiline=False, font_size = 18)
        self.a = App.get_running_app()
        self.make_activation_widget()

    def make_activation_widget(self):
        self.btn_submit = Button(text='Activate', font_size=18, background_color=(.7,.7,1,1))
        self.btn_submit.bind(on_release=self.get_user)
        self.btn_snooze = Button(text='Snooze', font_size=18, background_color=(.7,.7,1,1))
        self.btn_snooze.bind(on_release=self.snooze)
        self.gl = GridLayout(cols=2, height=125, size_hint_y=None)
        self.gl.add_widget(self.btn_snooze)
        self.gl.add_widget(self.btn_submit)

    def handle_input(self, *args):
        self.a.dest_user = self.txtinput.text
        self.txtinput.text=''
        self.manager.current = 'talk2'
        self.ids.bl_talk.padding = [0,0,0,0]
        self.ids.bl_talk.spacing = 0

    def get_user(self, *args):
        self.ids.bl_talk.remove_widget(self.gl)
        self.ids.bl_talk.padding = [70,70,70,70]
        self.ids.bl_talk.spacing = 50
        self.ids.bl_talk.add_widget(self.txtinput)
        self.txtinput.bind(on_text_validate = self.handle_input)
        self.ids.lbl_talk.text = 'Tell us which friend you want to send a message to!'

    def snooze(self, *args):
        if self.a.non_hardware:
            self.ids.bl_talk.remove_widget(self.gl)
        self.a.index = 'stretch'
        self.a.immediate = False
        self.a.cur_time += TIME_INTERVAL
        self.manager.current = 'wait'
        print('reminder snoozed')

    def wait_activate(self, *args):
        activate()
        self.a.listener.set_activated(False)
        t_now = time.time()
        while time.time() < (t_now +2*60):
            if self.a.listener.activated:
                break
            if self.a.listener.snoozed:
                break

    def check_activate(self, *args):
        if not self.t1.isAlive():
            Clock.unschedule(self.check_activate)
            if self.a.listener.activated:
                print('activated')
                Clock.schedule_once(self.get_user)
            else:
                print('not activated')
                Clock.schedule_once(self.snooze)

    def on_pre_enter(self, *args):
        print('entered talk screen')
        if self.a.non_hardware:
            self.ids.lbl_talk.text='Time to talk to friends!\nActivate sending a message using the buttons below.'
            self.ids.bl_talk.add_widget(self.gl)
        else:
            self.ids.lbl_talk.text = 'Time to talk to friends!\nActivate sending a message using the IMU.'
            self.t1 = threading.Thread(target=self.wait_activate, daemon=True)
            self.t1.start()
            Clock.schedule_interval(self.check_activate, .1)

class TalkScreen2(Screen):
    def __init__(self, **kw):
        super(TalkScreen2, self).__init__(**kw)
        self.lbl_speak = Label(text='Say \'start recording\' to send a message!',halign='center',font_size=20,color=(0,0,0,1))
        self.lbl_start_recog=Label(text='Start command recognized, get ready to send your message :)',halign='center',font_size=20,color=(0,0,0,1))
        self.lbl_start_not_recog=Label(text='Start command not recognized, please try again.',halign='center',font_size=20,color=(0,0,0,1))
        self.lbl_recording = Label(text='Send over an audio message! (Max: 10 seconds)',halign='center',font_size=20,color=(0,0,0,1))
        self.lbl_save=Label(text='Saving message transcription...',halign='center',font_size=20,color=(0,0,0,1))
        self.lbl_send = Label(text='Sending message...',halign='center',font_size=20,color=(0,0,0,1))
        self.a = App.get_running_app()

    def switch_congrats(self, *args):
        self.ids.box.remove_widget(self.lbl_send)
        self.a.completed = True
        self.manager.current = 'wait'

    def send_msg(self, *args):
        if self.a.dest_user == 'all':
            audio_topic = '/team2/network/audio'
            txt_topic = '/team2/network/text'
            self.a.listener.set_sent_from_me(True)
        else:
            audio_topic = '/' + self.a.dest_user + '/audio'
            txt_topic = '/' + self.a.dest_user + '/text'
        audio_path = self.a.speech_instance.get_audiopath()
        txt_path = self.a.speech_instance.get_txtpath()
        pub = PUB(audio_topic, "hello from audio")
        client = pub.connect_mqtt()
        client.loop_start()
        pub.publish_file(client, audio_path)
        client.disconnect()

        pub = PUB(txt_topic, self.a.dest_user + 'hello from txt')
        client = pub.connect_mqtt()
        client.loop_start()
        pub.publish_file(client, txt_path)
        client.disconnect()
        Clock.schedule_once(self.switch_congrats)

    def trans_send(self, *args):
        self.ids.box.remove_widget(self.lbl_save)
        self.ids.box.add_widget(self.lbl_send)
        Clock.schedule_once(self.send_msg)

    def transcribe_msg(self, *args):
        self.ids.box.remove_widget(self.lbl_recording)
        self.ids.box.add_widget(self.lbl_save)
        self.a.speech_instance.transcribe()
        Clock.schedule_once(self.trans_send)

    def record_msg(self, *args):
        print('recording...')
        self.a.speech_instance.record_msg()
        Clock.schedule_once(self.transcribe_msg)

    def cor_rec(self, *args):
        self.ids.box.remove_widget(self.lbl_start_recog)
        self.ids.box.add_widget(self.lbl_recording)
        Clock.schedule_once(self.record_msg)

    def correct(self, *args):
        print("Start command recognized!")
        try:
            self.ids.box.remove_widget(self.lbl_start_not_recog)
        except:
            print('got it first try gj')
        self.ids.box.remove_widget(self.lbl_speak)
        self.ids.box.add_widget(self.lbl_start_recog)
        Clock.schedule_once(self.cor_rec, 2)

    def not_correct(self, *args):
        self.ids.box.remove_widget(self.lbl_speak)
        self.ids.box.add_widget(self.lbl_speech)
        try:
            self.ids.box.add_widget(self.lbl_start_not_recog)
        except:
            print('you already messed up once my dude')
        print("Start command not recognized...")
        Clock.schedule_once(self.recognize_start, .1)

    def recognize_start(self, *args):
        for j in range(1):
            print('Speak!')
            time.sleep(0.5)
            guess = self.a.speech_instance.recognize_speech_from_mic()
            if guess["transcription"]:
                break
            if not guess["success"]:
                break
            print("I didn't catch that. What did you say?\n")
            if guess["error"]:
                print("ERROR: {}".format(guess["error"]))
                break
        try:
            self.ids.box.remove_widget(self.lbl_speech)
            self.ids.box.add_widget(self.lbl_speak)
        except:
            print('first run')

        msg = "You said: {}".format(guess["transcription"])
        self.lbl_speech = Label(text=msg,halign='center',font_size=20,color=(0,0,0,1))
        print(msg)

        if str(guess["transcription"]).find("start recording") != -1:
            Clock.schedule_once(self.correct)
        else:
            Clock.schedule_once(self.not_correct)

    def on_enter(self, *args):
        print("calling talking to friends exercise")
        self.ids.box.add_widget(self.lbl_speak)
        Clock.schedule_once(self.recognize_start, .1)

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
        self.a = App.get_running_app()

    def switch_congrats(self, *args):
        self.a.completed = True
        self.manager.current = 'wait'

    def activity(self, *args):
        exercise_stretch()
        Clock.schedule_once(self.switch_congrats)

    def snooze(self, *args):
        if self.a.non_hardware:
            self.ids.bl_stretch.remove_widget(self.gl)
        self.a.index = 'stretch'
        self.a.immediate = False
        self.a.cur_time += TIME_INTERVAL
        self.manager.current = 'wait'
        print('reminder snoozed')

    def transition(self, *args):
        self.ids.bl_stretch.remove_widget(self.gl)
        self.ids.lbl_stretch.text = 'Stretching activated!\n\nYou have around 30 seconds to get your area ready.\nMake sure your entire body is in clear view of your webcam.'
        Clock.schedule_once(self.activity)

    def check_activate(self, *args):
        if not self.t1.isAlive():
            Clock.unschedule(self.check_activate)
            if self.a.listener.activated:
                Clock.schedule_once(self.transition)
            else:
                Clock.schedule_once(self.snooze)

    def wait_activate(self, *args):
        activate()
        self.a.listener.set_activated(False)
        t_now = time.time()
        while time.time() < (t_now +2*60):
            if self.a.listener.activated:
                break
            if self.a.listener.snoozed:
                break

    def on_pre_enter(self, *args):
        print('entered stretch screen')
        if self.a.non_hardware:
            self.ids.lbl_stretch.text='Time to stretch!\nActivate using the buttons below.'
            self.ids.bl_stretch.add_widget(self.gl)
        else:
            self.ids.lbl_stretch.text='Time to stretch!\nActivate using the IMU.'
            self.t1=threading.Thread(target=self.wait_activate, daemon=True)
            self.t1.start()
            Clock.schedule_interval(self.check_activate, 0.1)

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
        self.a = App.get_running_app()

    def switch_congrats(self, *args):
        self.a.completed = True
        self.manager.current = 'wait'

    def snooze(self, *args):
        if self.a.non_hardware:
            self.ids.bl_breathe.remove_widget(self.gl)
        self.a.index = 'stretch'
        self.a.immediate = False
        self.a.cur_time += TIME_INTERVAL
        self.manager.current = 'wait'
        print('reminder snoozed')

    def activity_software2 (self, *args):
        self.manager.current = 'ball'

    def activity_software(self, *args):
        self.ids.bl_breathe.remove_widget(self.gl)
        self.ids.lbl_breathe.text = 'Breathe with the ball on the screen.'
        Clock.schedule_once(self.activity_software2, 3.5)

    def activity(self, *args):
        self.ids.lbl_breathe.text = 'Follow along with the breathing exercise on the matrix!'
        exercise_breathe()
        Clock.schedule_once(self.switch_congrats, 30)

    def wait_activate(self, *args):
        activate()
        self.a.listener.set_activated(False)
        t_now = time.time()
        while time.time() < (t_now +2*60):
            if self.a.listener.activated:
                break
            if self.a.listener.snoozed:
                break

    def check_activate(self, *args):
        if not self.t1.isAlive():
            Clock.unschedule(self.check_activate)
            if self.a.listener.activated:
                Clock.schedule_once(self.activity)
            else:
                Clock.schedule_once(self.snooze)

    def on_pre_enter(self, *args):
        print('entered breathe screen')
        if self.a.non_hardware:
            self.ids.lbl_breathe.text='Time to breathe!\nActivate using the buttons below.'
            self.ids.bl_breathe.add_widget(self.gl)
        else:
            self.ids.lbl_breathe.text='Time to breathe!\nActivate using the IMU.'
            self.t1=threading.Thread(target=self.wait_activate, daemon=True)
            self.t1.start()
            Clock.schedule_interval(self.check_activate, 0.1)

class BallScreen(Screen):
    def __init__(self, **kw):
        super(BallScreen, self).__init__(**kw)
        self.size_ball_x = 101
        self.size_ball_y = 101
        self.inc = True
        self.a= App.get_running_app()

    def switch_congrats(self, *args):
        self.canvas.clear()
        Clock.unschedule(self.ball)
        self.a.completed = True
        self.manager.current = 'wait'

    def ball(self, *args):
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
    first_run = True

    listener = Listener()
    speech_instance = speech('Message')
    rpi_conn = rpi_conn()

    def build(self):
        return Root()

if __name__ == '__main__':
    WAP().run()
