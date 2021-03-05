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
from kivy.core.window import Window
from helper import *
from functools import partial
from kivy.uix.textinput import TextInput
from kivy.uix.checkbox import CheckBox
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Ellipse
from kivy.uix.image import Image
from test_msg_sub import Listener
import threading
from playsound import playsound
import glob
import os
from MQTT.pub import PUB
try:
    from Speech.audio_msg import speech
except:
    from Team2.Speech.audio_msg import speech
from rpi_conn import rpi_conn

from Stats.stats import *

Builder.load_file('./UI/screen.kv')
TIME_INTERVAL = 30

class LoginScreen(Screen):
    def __init__(self, **kw):
        super(LoginScreen, self).__init__(**kw)
        self.a = App.get_running_app()

    def update(self):
        userID = self.ids.login.text
        if os.path.exists('config.txt'):
            config = open('config.txt', 'r')
            self.a.mode = config.readline().split('=')[1].replace('\n', '')
            self.a.userID = config.readline().split('=')[1].replace('\n', '')
            self.a.ip = config.readline().split('=')[1].replace('\n', '')
            self.a.port = config.readline().split('=')[1].replace('\n', '')
            config.close()

        if(userID !=''):
            self.a.userID = userID
            config = open('config.txt', 'w')
            config_txt = 'mode=' + self.a.mode + '\n' + 'ID=' + self.a.userID + '\n' + 'ip=' + self.a.ip + '\n' + 'port=' + self.a.port
            config.write(config_txt)
            config.close()
            self.ids.login.background_color = (1, 1, 1, 1)
            self.manager.current = 'version'
            self.manager.transition.direction = 'left'
        else:
            self.ids.login.background_color = (1, 0, 0, .3)
            print('blank userID')

        #update user stat id
        self.a.user_stat.user_id = self.a.userID

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
        self.a.ip = self.ids.ip.text
        self.a.port = self.ids.port.text
        self.user = self.ids.user.text
        self.pw = self.ids.pw.text
        if self.a.ip == '' or self.a.port == '' or self.user == '' or self.pw == '':
            if self.ip =='':
                self.ids.ip.background_color = (1, 0, 0, .3)
            if self.port == '':
                self.ids.port.background_color = (1, 0, 0, .3)
            if self.user == '':
                self.ids.user.background_color = (1, 0, 0, .3)
            if self.pw == '':
                self.ids.pw.background_color = (1, 0, 0, .3)
        else:
            f = open('config.txt', 'w')
            config_txt = 'mode=' + self.a.mode + '\n' + 'ID=' + self.a.userID + '\n' + 'ip=' + self.a.ip + '\n' + 'port=' + self.a.port
            f.write(config_txt)
            f.close()
            self.a.rpi_conn.set_conn_info(str(self.a.ip), int(self.a.port), str(self.user), str(self.pw))
            self.t1 = threading.Thread(target=self.a.rpi_conn.connect, daemon=True)
            self.t1.start()
            Clock.schedule_interval(self.connect, .1)

    def on_pre_enter(self):
        self.ids.ip.text = self.a.ip
        self.ids.port.text = self.a.port

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

    def switch_forward(self, *args):
        if self.a.big_dict['stretch'][0]:
            for k,v in self.a.big_dict.items():
                if v[0]:
                    self.ids.gl.remove_widget(self.widgets[k][0])
                    self.ids.gl.remove_widget(self.widgets[k][1])
            self.manager.current = 'config'
            self.manager.transition.direction='left'
        else:
            self.manager.current = 'wait'
            self.manager.transition.direction='left'

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

class ConfigScreen(Screen):
    def __init__(self, **kw):
        super(ConfigScreen, self).__init__(**kw)
        self.config = False
        self.img = Image(source = './UI/guidance.png')

    def quit(self):
        sys.exit(0)

    def switch_back(self, *args):
        self.manager.current = 'time'
        self.manager.transition.direction='right'

    def calibrate(self, *args):
        config_stretch()
        Clock.schedule_once(self.switch_forward)

    def ping(self, type):
        self.config = type

    def pre_calibrate(self, *args):
        if self.config:
            self.ids.big_lbl.text = 'Mimic the following poses when prompted! Make sure your entire body is in view.'
            self.ids.small_lbl.text = 'Note: it may take a few seconds for the separate calibration window to pop up.'
            self.ids.bl.remove_widget(self.ids.small_lbl)
            self.ids.bl.remove_widget(self.ids.activation_gl)
            self.ids.bl.remove_widget(self.ids.check_gl)
            self.ids.bl.add_widget(self.img)
            self.ids.bl.add_widget(self.ids.small_lbl)
            Clock.schedule_once(self.calibrate)
        else:
            Clock.schedule_once(self.switch_forward)

    def switch_forward(self, *args):
        self.manager.current = 'wait'
        self.manager.transition.direction='left'

class WaitScreen(Screen):
    def __init__(self, **kw):
        super(WaitScreen, self).__init__(**kw)
        self.lbl_normal=Label(text='Thank you for selecting your wellness actions!\nYou will be reminded to focus on these throughout the day.',halign='center',font_size=20,color=(0,0,0,1))
        self.a = App.get_running_app()
        self.time_elapsed = time.time()
        self.sender = ''
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

    def switch_check(self, *args):
        self.manager.transition = NoTransition()
        self.manager.current = 'check'
        Clock.unschedule(self.check_for_messages)
        Clock.unschedule(self.check_others_finished)

    def switch_congrats(self, *args):
        self.manager.current = 'congrats'
        Clock.unschedule(self.check_for_messages)
        Clock.unschedule(self.check_others_finished)

    def reschedule_activity(self, *args):
        if self.mode == 'limited':
            print(f'entered limited, run num: {self.run_num}')
            if self.run_num > 0:
                Clock.schedule_once(self.switch_check, max(0, (TIME_INTERVAL - self.time_elapsed)))
                print(f'time elapsed from last activity: {self.time_elapsed}')
                print(f'time remaining: {TIME_INTERVAL - self.time_elapsed}')
            else:
                print('waitscreen forever')
            self.run_num -=1
        elif self.mode == 'debug':
            if self.debug_mode == 'seconds':
                print('entered waitscreen debug seconds')
                Clock.schedule_once(self.switch_check, max(0, (TIME_INTERVAL - self.time_elapsed)))
                print(f'time elapsed from last activity: {self.time_elapsed}')
                print(f'time remaining: {TIME_INTERVAL - self.time_elapsed}')
            else:
                print('entered waitscreen debug minutes')
                Clock.schedule_once(self.switch_check,max(0, (TIME_INTERVAL*6 - self.time_elapsed)))
                print(f'time elapsed from last activity: {self.time_elapsed}')
                print(f'time remaining: {TIME_INTERVAL*6 - self.time_elapsed}')
        else:
            print('entered watiscreen reg')
            Clock.schedule_once(self.switch_check, max(0, (TIME_INTERVAL*60 - self.a.time_elapsed - self.time_elapsed)))
            print(f'time elapsed from last activity: {self.time_elapsed}')
            print(f'time remaining: {TIME_INTERVAL*60 - self.time_elapsed-self.a.time_elapsed}')

    def update_screen_snooze(self, *args):
        self.ids.img_wait.source = 'UI/face.png'
        if self.a.non_hardware:
            Clock.unschedule(self.update_screen_snooze)
            self.ids.boxy.remove_widget(self.lbl_friend_finished)
            self.ids.boxy.remove_widget(self.gl)
        else:
            self.ids.boxy.remove_widget(self.lbl_friend_finished_hardware)
        self.ids.boxy.add_widget(self.lbl_normal)
        Clock.schedule_interval(self.check_for_messages, 1)
        Clock.schedule_interval(self.check_others_finished, 1)
        self.time_elapsed = time.time() - self.time_elapsed
        Clock.schedule_once(self.reschedule_activity)

    def update_screen_completed(self, *args):
        self.ids.img_wait.source = 'UI/face.png'
        self.ids.boxy.remove_widget(self.lbl_send)
        self.ids.boxy.add_widget(self.lbl_normal)
        Clock.schedule_interval(self.check_for_messages, 1)
        Clock.schedule_interval(self.check_others_finished, 1)
        self.time_elapsed = time.time() - self.time_elapsed
        Clock.schedule_once(self.reschedule_activity)

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

    #a.listener.dest_user
    def send_msg(self, *args):
        audio_topic = '/' + self.a.dest_user + '/audio/' + self.a.userID
        txt_topic = '/' + self.a.dest_user + '/text/' + self.a.userID
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
        Clock.schedule_once(self.update_screen_completed)

    def trans_send(self, *args):
        self.ids.boxy.remove_widget(self.lbl_save)
        self.ids.boxy.add_widget(self.lbl_send)
        Clock.schedule_once(self.send_msg)

    def transcribe_msg(self, *args):
        self.ids.boxy.remove_widget(self.lbl_recording)
        self.ids.boxy.add_widget(self.lbl_save)
        transcribed_msg = self.a.speech_instance.transcribe()
        self.a.user_stat.addMessage(SENT, self.a.dest_user, transcribed_msg)
        self.a.user_stat.addTask([TALKING_TO_FRIENDS])
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
        # self.ids.boxy2.remove_widget(self.ids.img_wait)
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
            Clock.unschedule(self.update_screen_snooze)
            self.ids.boxy.remove_widget(self.lbl_friend_finished)
            self.ids.boxy.remove_widget(self.gl)
        else:
            self.ids.boxy.remove_widget(self.lbl_friend_finished_hardware)
        self.ids.boxy.add_widget(self.lbl_speak)
        Clock.schedule_once(self.recognize_start, .1)

    def check_others_finished(self, *args):
        if len(self.a.listener.congrats_ppl) > 0:
            Clock.unschedule(self.check_for_messages)
            Clock.unschedule(self.check_others_finished)
            Clock.unschedule(self.switch_check)
            self.a.dest_user = self.a.listener.congrats_ppl[0]
            print(self.a.dest_user)
            self.a.listener.congrats_ppl.pop(0)
            self.ids.boxy.remove_widget(self.lbl_normal)
            print('SOMEBODY FINISHED SMTHG WOWOWOWOW')
            if self.a.non_hardware:
                print('entered non hardware')
                try:
                    self.ids.boxy.remove_widget(self.lbl_friend_finished)
                except:
                    pass
                msg = 'Your friend ' + self.a.dest_user + ' just completed a task!\n Activate using the buttons if you want to send a message to them.'
                self.lbl_friend_finished = Label(text=msg,halign='center',font_size=20,color=(0,0,0,1))
                self.ids.img_wait.source = 'UI/speech.png'
                self.ids.boxy.add_widget(self.lbl_friend_finished)
                Clock.schedule_once(self.update_screen_snooze, 2*60)
                try:
                    self.ids.boxy.add_widget(self.gl)
                except:
                    pass
            else:
                print('entered hardware')
                msg = 'Your friend ' + self.a.dest_user + ' just completed a task!\n Activate using the IMU if you want to send a message to them.'
                self.lbl_friend_finished_hardware = Label(text=msg,halign='center',font_size=20,color=(0,0,0,1))
                self.ids.img_wait.source = 'UI/speech.png'
                self.ids.boxy.add_widget(self.lbl_friend_finished_hardware)
                self.t1 = threading.Thread(target=self.wait_for_activate, daemon=True)
                self.t1.start()
                Clock.schedule_interval(self.check_hardware_activate, .1)

    def update_screen(self,*args):
        self.ids.img_wait.source = 'UI/face.png'
        try:
            latest_audio = max(glob.iglob('./RecAudio/'+self.sender+'*'), key=os.path.getctime)
            print(f'playing ... `{latest_audio}`' )
            playsound(latest_audio, True)
        except:
            print('error: audio could not play')
            e = sys.exc_info()[0]
            print(f'error msg: {e}')
        self.ids.boxy.remove_widget(self.lbl_msg)
        try:
            self.ids.boxy.add_widget(self.lbl_normal)
        except:
            pass
        file_path = './RecTxt/' + self.sender + '*'
        remaining_files = glob.glob(file_path)
        for f in remaining_files:
            os.remove(f)
        Clock.schedule_interval(self.check_for_messages, 1)
        Clock.schedule_interval(self.check_others_finished, 1)

    #received
    def check_for_messages(self, *args):
        if os.path.exists('./RecTxt'):
            if os.listdir('./RecTxt'):
                Clock.unschedule(self.check_for_messages)
                Clock.unschedule(self.check_others_finished)
                try:
                    latest_txt = max(glob.iglob('./RecTxt/*'), key=os.path.getctime)
                    self.sender = str(os.path.split(latest_txt)[1].split('_')[0])
                    if self.sender != self.a.userID:
                        print(f'received msg from `{self.sender}`')
                        f = open(latest_txt)
                        msg = f.readline()
                        display_msg = 'Your friend ' + self.sender + ' said:\n' + msg
                        print(display_msg)

                        #Received a message
                        self.a.user_stat.addMessage(RECEIVED, self.sender, msg)

                        self.lbl_msg = Label(text=display_msg,halign='center',font_size=20,color=(0,0,0,1))
                        self.ids.boxy.remove_widget(self.lbl_normal)
                        self.ids.boxy.add_widget(self.lbl_msg)
                        Clock.schedule_once(self.update_screen)
                    else:
                        file_path = './RecTxt/' + self.sender + '*'
                        remaining_files = glob.glob(file_path)
                        for f in remaining_files:
                            os.remove(f)
                except:
                    pass

    def on_pre_enter(self, *args):
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
            if self.a.mode.find('limited') != -1:
                self.mode = self.a.mode.split(',')[0]
                self.run_num = int(self.a.mode.split(',')[1])
            elif self.a.mode.find('debug') != -1:
                self.mode = self.a.mode.split(',')[0]
                self.debug_mode = self.a.mode.split(',')[1]
            else:
                self.mode = self.a.mode

        if self.a.immediate:
            Clock.schedule_once(self.switch_check)
        else:
            if self.a.completed:
                self.time_elapsed = time.time() - self.time_elapsed
                Clock.schedule_once(self.switch_congrats)
                self.a.completed = False
            else:
                Clock.schedule_interval(self.check_for_messages, 1)
                Clock.schedule_interval(self.check_others_finished, 1)
                self.time_elapsed = time.time()
                if self.mode == 'limited':
                    print(f'entered limited, run num: {self.run_num}')
                    if self.run_num > 0:
                        Clock.schedule_once(self.switch_check, TIME_INTERVAL)
                    else:
                        print('waitscreen forever')
                    self.run_num -=1
                elif self.mode == 'debug':
                    if self.debug_mode == 'seconds':
                        print('entered waitscreen debug seconds')
                        Clock.schedule_once(self.switch_check, TIME_INTERVAL)
                    else:
                        print('entered waitscreen debug minutes')
                        Clock.schedule_once(self.switch_check, TIME_INTERVAL*6)
                else:
                    print('entered waitscreen regular')
                    Clock.schedule_once(self.switch_check, TIME_INTERVAL*60 - self.a.time_elapsed)

class CheckScreen(Screen):
    def __init__(self, **kw):
        super(CheckScreen, self).__init__(**kw)
        self.a = App.get_running_app()

    def switch_screen(self, activity, *largs):
        self.manager.transition = SlideTransition()
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
        if self.a.non_hardware:
            Clock.unschedule(self.snooze)
            self.ids.bl_talk.remove_widget(self.gl)
        self.ids.bl_talk.padding = [70,70,70,70]
        self.ids.bl_talk.spacing = 50
        self.ids.bl_talk.add_widget(self.txtinput)
        self.txtinput.bind(on_text_validate = self.handle_input)
        self.ids.bl2_talk.remove_widget(self.ids.img_talk)
        self.ids.lbl_talk.text = 'Tell us which friend you want to send a message to!'

    def snooze(self, *args):
        if self.a.non_hardware:
            Clock.unschedule(self.snooze)
            self.ids.bl_talk.remove_widget(self.gl)
        #self.a.index = 'stretch'
        #self.a.immediate = False
        #self.a.cur_time += TIME_INTERVAL
        self.manager.current = 'snooze'
        print('reminder snoozed')

    def wait_activate(self, *args):
        activate(self.a.userID)
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
                Clock.schedule_once(self.get_user)
                self.a.listener.set_activated(False)
            else:
                Clock.schedule_once(self.snooze)
                self.a.listener.set_snoozed(False)

    def on_leave(self, *args):
        self.ids.bl_talk.remove_widget(self.txtinput)

    def on_pre_enter(self, *args):
        print('entered talk screen')
        win_width, win_height = Window.size
        if self.a.non_hardware:
            self.ids.bl2_talk.remove_widget(self.ids.img_talk)
            self.ids.bl2_talk.add_widget(self.ids.img_talk)
            self.ids.bl2_talk.remove_widget(self.ids.lbl_talk)
            self.ids.bl2_talk.add_widget(self.ids.lbl_talk)
            self.ids.lbl_talk.text='Time to talk to friends!\nActivate sending a message using the buttons below.'
            try:
                self.ids.bl2_talk.padding = [0,0,0,win_height/4]
                self.ids.bl_talk.add_widget(self.gl)
            except:
                pass
            Clock.schedule_once(self.snooze, 2*60)
        else:
            self.ids.bl2_talk.remove_widget(self.ids.img_talk)
            self.ids.bl2_talk.remove_widget(self.ids.lbl_talk)
            self.ids.bl2_talk.add_widget(self.ids.img_talk)
            self.ids.bl2_talk.add_widget(self.ids.lbl_talk)
            self.ids.bl2_talk.padding = [0,0,0,win_height/3]
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


    #Sent a message
    def send_msg(self, *args):
        if self.a.dest_user == 'all':
            audio_topic = '/team2/network/audio/' + self.a.userID
            txt_topic = '/team2/network/text/' + self.a.userID
        else:
            audio_topic = '/' + self.a.dest_user + '/audio/' + self.a.userID
            txt_topic = '/' + self.a.dest_user + '/text/' + self.a.userID
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

        #Sent message

    def transcribe_msg(self, *args):
        self.ids.box.remove_widget(self.lbl_recording)
        self.ids.box.add_widget(self.lbl_save)

        transcribed_msg = self.a.speech_instance.transcribe()
        self.a.user_stat.addMessage(SENT, self.a.dest_user, transcribed_msg)
        self.a.user_stat.addTask([TALKING_TO_FRIENDS])
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
        #Ends stretching
        self.a.user_stat.addTask([STRETCHING])

    def activity(self, *args):
        exercise_stretch()
        Clock.schedule_once(self.switch_congrats)

    def snooze(self, *args):
        if self.a.non_hardware:
            Clock.unschedule(self.snooze)
            self.ids.bl_stretch.remove_widget(self.gl)
        #self.a.index = 'stretch'
        #self.a.immediate = False
        #self.a.cur_time += TIME_INTERVAL
        self.manager.current = 'snooze'
        print('reminder snoozed')

    def transition(self, *args):
        win_width, win_height = Window.size
        self.ids.bl2_stretch.remove_widget(self.ids.img_stretch)
        if self.a.non_hardware:
            Clock.unschedule(self.snooze)
            self.ids.bl_stretch.remove_widget(self.gl)
        self.ids.lbl_stretch.text = 'Stretching activated!\n\nYou have around 30 seconds to get your area ready.\nMake sure your entire body is in clear view of your webcam.'
        self.ids.bl2_stretch.padding = [0,0,0,win_height/3]
        Clock.schedule_once(self.activity)

    def check_activate(self, *args):
        if not self.t1.isAlive():
            Clock.unschedule(self.check_activate)
            if self.a.listener.activated:
                Clock.schedule_once(self.transition)
                self.a.listener.set_activated(False)
            else:
                Clock.schedule_once(self.snooze)
                self.a.listener.set_snoozed(False)

    def wait_activate(self, *args):
        activate(self.a.userID)
        self.a.listener.set_activated(False)
        t_now = time.time()
        while time.time() < (t_now +2*60):
            if self.a.listener.activated:
                break
            if self.a.listener.snoozed:
                break

    def on_pre_enter(self, *args):
        print('entered stretch screen')
        win_width, win_height = Window.size
        if self.a.non_hardware:
            self.ids.bl2_stretch.remove_widget(self.ids.img_stretch)
            self.ids.bl2_stretch.remove_widget(self.ids.lbl_stretch)
            self.ids.bl2_stretch.add_widget(self.ids.img_stretch)
            self.ids.bl2_stretch.add_widget(self.ids.lbl_stretch)
            self.ids.lbl_stretch.text='Time to stretch!\nActivate using the buttons below.'
            try:
                self.ids.bl2_stretch.padding = [0,0,0,win_height/4]
                self.ids.bl_stretch.add_widget(self.gl)
            except:
                pass
            Clock.schedule_once(self.snooze, 2*60)
        else:
            self.ids.bl2_stretch.remove_widget(self.ids.img_stretch)
            self.ids.bl2_stretch.remove_widget(self.ids.lbl_stretch)
            self.ids.bl2_stretch.add_widget(self.ids.img_stretch)
            self.ids.bl2_stretch.add_widget(self.ids.lbl_stretch)
            self.ids.bl2_stretch.padding = [0,0,0,win_height/3]
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
        self.ids.img_breathe.source = 'UI/clock.png'

    def snooze(self, *args):
        if self.a.non_hardware:
            Clock.unschedule(self.snooze)
            self.ids.bl_breathe.remove_widget(self.gl)
        #self.a.index = 'stretch'
    #    self.a.immediate = False
    #    self.a.cur_time += TIME_INTERVAL
        self.manager.current = 'snooze'
        print('reminder snoozed')

    def activity_software2 (self, *args):
        self.manager.current = 'ball'
        # Fix: Looks kind of weird still
        win_width, win_height = Window.size
        self.ids.bl2_breathe.remove_widget(self.ids.lbl_breathe)
        self.ids.bl2_breathe.add_widget(self.ids.img_breathe)
        self.ids.bl2_breathe.add_widget(self.ids.lbl_breathe)
        # self.ids.bl_breathe.remove_widget(self.ids.bl2_breathe)
        # self.ids.bl_breathe.add_widget(self.ids.bl2_breathe)

    def activity_software(self, *args):
        if self.a.non_hardware:
            Clock.unschedule(self.snooze)
            self.ids.bl_breathe.remove_widget(self.gl)
        self.ids.bl2_breathe.remove_widget(self.ids.img_breathe)
        self.ids.lbl_breathe.text = 'Breathe with the ball on the screen.'
        #finished breathing
        self.a.user_stat.addTask([BREATHING])
        # self.ids.lbl_breathe.size_hint = (1, 1)
        # self.ids.bl2_breathe.padding = [0,0,0,0]
        Clock.schedule_once(self.activity_software2, 3.5)

    def activity(self, *args):
        win_width, win_height = Window.size
        self.ids.bl2_breathe.padding = [0,0,0,win_height/3]
        self.ids.img_breathe.source = 'UI/matrix.png'
        self.ids.lbl_breathe.text = 'Follow along with the breathing exercise on the matrix!'
        exercise_breathe(self.a.userID)

        Clock.schedule_once(self.switch_congrats, 30)

    def wait_activate(self, *args):
        activate(self.a.userID)
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
                self.a.listener.set_activated(False)
            else:
                Clock.schedule_once(self.snooze)
                self.a.listener.set_snoozed(False)

    def on_pre_enter(self, *args):
        print('entered breathe screen')
        win_width, win_height = Window.size
        if self.a.non_hardware:
            self.ids.bl2_breathe.remove_widget(self.ids.img_breathe)
            self.ids.bl2_breathe.add_widget(self.ids.img_breathe)
            self.ids.bl2_breathe.remove_widget(self.ids.lbl_breathe)
            self.ids.bl2_breathe.add_widget(self.ids.lbl_breathe)
            self.ids.lbl_breathe.text='Time to breathe!\nActivate using the buttons below.'
            try:
                self.ids.bl2_breathe.padding = [0,0,0,win_height/4]
                self.ids.bl_breathe.add_widget(self.gl)
            except:
                pass
            Clock.schedule_once(self.snooze, 2*60)
        else:
            self.ids.bl2_breathe.remove_widget(self.ids.img_breathe)
            self.ids.bl2_breathe.remove_widget(self.ids.lbl_breathe)
            self.ids.bl2_breathe.add_widget(self.ids.img_breathe)
            self.ids.bl2_breathe.add_widget(self.ids.lbl_breathe)
            self.ids.bl2_breathe.padding = [0,0,0,win_height/3]
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
        self.time = 0
        self.time2 = 30
        self.cnt = 0
        self.a= App.get_running_app()

    def switch_congrats(self, *args):
        self.cnt = 0
        self.time = 0
        self.time2 = 30
        self.canvas.clear()
        Clock.unschedule(self.ball)
        self.a.completed = True
        self.manager.current = 'wait'

    def ball(self, *args):
        self.canvas.clear()
        self.cnt += 1
        with self.canvas:
            Color(.7,.7,1,1)
            Ellipse(pos= (self.center_x - (self.size_ball_x/2), self.center_y - (self.size_ball_y/2)), size=(self.size_ball_x,self.size_ball_y))
            #Label(text=str(self.time),pos= (self.center_x - (101/2), self.center_y - (101/2)), font_size=24, color = (0,0,0,1))
            Label(text = str(self.time2), pos= (10,10), font_size=24, color = (0,0,0,1))
        if self.size_ball_x == 200 or self.size_ball_x == 100:
            self.inc = not self.inc
        if not self.inc:
            self.size_ball_x += 1
            self.size_ball_y += 1
        else:
            self.size_ball_x -= 1
            self.size_ball_y -= 1
        if self.cnt % 20 == 0:
            self.time2 -= 1
            if self.inc:
                self.time -= 1
            else:
                self.time += 1

    def on_enter(self):
        Clock.schedule_interval(self.ball, .05)
        Clock.schedule_once(self.switch_congrats, 30)

class CongratsScreen(Screen):
    def __init__(self, **kw):
        super(CongratsScreen, self).__init__(**kw)
        self.a = App.get_running_app()

    def switch_screen(self, *args):
        self.manager.current = 'wait'

    def on_enter(self, *args):
        congrats(self.a.userID)
        Clock.schedule_once(self.switch_screen, 5)

class SnoozeScreen(Screen):
    def __init__(self, **kw):
        super(SnoozeScreen, self).__init__(**kw)

    def switch_screen(self, *args):
        self.manager.current = 'wait'

    def on_enter(self, *args):
        Clock.schedule_once(self.switch_screen, 3)

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

    userID = ''
    mode = ''
    ip=''
    port = ''
    dest_user = ''
    non_hardware = False
    first_run = True

    listener = Listener()
    speech_instance = speech('Message')

    user_stat = userStats()
    rpi_conn = rpi_conn()

    def build(self):
        return Root()

if __name__ == '__main__':
    WAP().run()
