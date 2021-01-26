import sys
import time
import pyaudio
import speech_recognition as sr
import pathlib
from os import path
from scipy.io.wavfile import write

# Prompt limit for voice command
PROMPT_LIMIT=1
# SAVING .WAV FILE GLOBAL VARIABLES
sent_audiodir = "./Speech/SentAudio"
sent_txtdir = "./Speech/SentTxt"
txt_suffix = "txt"
audio_suffix = "wav"
msg_limit=10 #in seconds - length of audio message
listen_limit=3 # in seconds - if no audio is detected, stop recording

class speech:
    def __init__(self, filename):
        # Filename is the audio filename WITHOUT the file extension
        base_audioname = filename
        # Check if directory exists, if not create it, if does continue
        pathlib.Path(sent_audiodir).mkdir(parents=True, exist_ok=True)
        audio_path = path.join(sent_audiodir, base_audioname + "." + audio_suffix)

        pathlib.Path(sent_txtdir).mkdir(parents=True, exist_ok=True)
        txt_path = path.join(sent_txtdir, base_audioname + "_transcript" + "." + txt_suffix)

        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.audio_file = audio_path
        self.txt_file = txt_path

    def get_audiopath(self):
        return self.audio_file

    def get_txtpath(self):
        return self.txt_file

    def recognize_speech_from_mic(self):
        """Transcribe speech from recorded from `microphone`.

        Returns a dictionary with three keys:
        "success": a boolean indicating whether or not the API request was
                   successful
        "error":   `None` if no error occured, otherwise a string containing
                   an error message if the API could not be reached or
                   speech was unrecognizable
        "transcription": `None` if speech could not be transcribed,
                   otherwise a string containing the transcribed text
        """
        # check that recognizer and microphone arguments are appropriate type
        if not isinstance(self.recognizer, sr.Recognizer):
            raise TypeError("`recognizer` must be `Recognizer` instance")

        if not isinstance(self.microphone, sr.Microphone):
            raise TypeError("`microphone` must be `Microphone` instance")

        # adjust the recognizer sensitivity to ambient noise and record audio
        # from the microphone
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source)

        # set up the response object
        response = {
            "success": True,
            "error": None,
            "transcription": None
        }

        # try recognizing the speech in the recording
        # if a RequestError or UnknownValueError exception is caught,
        #     update the response object accordingly
        try:
            response["transcription"] = self.recognizer.recognize_google(audio)
        except sr.RequestError:
            # API was unreachable or unresponsive
            response["success"] = False
            response["error"] = "API unavailable"
        except sr.UnknownValueError:
            # speech was unintelligible
            response["error"] = "Unable to recognize speech"

        return response

    def record_msg(self):
        with self.microphone as source:
            print("Send over an audio message! (Max: 10 seconds)")
            try:
                start_time = time.time()
                audio = self.recognizer.listen(source, listen_limit, msg_limit)
            except sr.WaitTimeoutError:
                print("No audio detected...Try again...")

        print("Recording finished!")

        # write audio to a WAV file
        with open(self.audio_file, "wb") as f:
            f.write(audio.get_wav_data())

    def transcribe(self):
            # AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), self.audio_file)
            with sr.AudioFile(self.audio_file) as source:
                audio = self.recognizer.record(source)

            with open(self.txt_file, "w") as f:
                try:
                    print('Saving message transcription...')
                    f.write(self.recognizer.recognize_google(audio))
                    f.close()
                except sr.UnknownValueError:
                    print("Google Speech Recognition could not understand audio")
                except sr.RequestError as e:
                    print("Could not request results from Google Speech Recognition service; {0}".format(e))

    def recognize_start(self):
        recognized = False
        while not recognized:
            # Listen for voice command before starting recording
            for j in range(PROMPT_LIMIT):
                print('Speak!')
                time.sleep(0.5)
                guess = self.recognize_speech_from_mic()
                if guess["transcription"]:
                    break
                if not guess["success"]:
                    break
                print("I didn't catch that. What did you say?\n")

                if guess["error"]:
                    print("ERROR: {}".format(guess["error"]))
                    break

            # Debug statement
            print("You said: {}".format(guess["transcription"]))

            if str(guess["transcription"]).find("start recording") != -1:
                print("Start command recognized!")
                recognized = True
                break
            else:
                print("Start command not recognized...")
                recognized = False

        return recognized

    def main_record(self):
        # "Start recording" voice command recognized!
        if self.recognize_start():
            time.sleep(2)
            print('Recording...')

            #save audio message as .wav file
            self.record_msg()

            # transcribe the audio message + save into a file
            self.transcribe()

if __name__ == "__main__":
    speech_instance = speech("message")
    speech_instance.msg_flow()
