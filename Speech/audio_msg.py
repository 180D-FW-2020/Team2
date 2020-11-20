import time
import pyaudio
import speech_recognition as sr
from os import path
from scipy.io.wavfile import write


# SAVING .WAV FILE GLOBAL VARIABLES
msg_limit=10 #in seconds - length of audio message
listen_limit=3 # in seconds - if no audio is detected, stop recording


def recognize_speech_from_mic(recognizer, microphone):
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
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")

    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")

    # adjust the recognizer sensitivity to ambient noise and record audio
    # from the microphone
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

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
        response["transcription"] = recognizer.recognize_google(audio)
    except sr.RequestError:
        # API was unreachable or unresponsive
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        # speech was unintelligible
        response["error"] = "Unable to recognize speech"

    return response

def record_msg(recognizer, microphone, audio_file):
    with microphone as source:
        print("Send over an audio message! (Max: 10 seconds)")
        try:
            start_time = time.time()
            audio = recognizer.listen(source, listen_limit, msg_limit)
        except sr.WaitTimeoutError:
            print("No audio detected...Try again...")

    print("Recording finished!")

    # write audio to a WAV file
    with open(audio_file, "wb") as f:
        f.write(audio.get_wav_data())

def transcribe(recognizer, microphone, audio_file):
        AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), audio_file)
        with sr.AudioFile(AUDIO_FILE) as source:
            audio = recognizer.record(source)

        text_name="transcript.txt"
        with open(text_name, "w") as f:
            try:
                print('Saving message transcription...')
                f.write(recognizer.recognize_google(audio))
                f.close()
            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio")
            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))

def main_msg():
    # recognize start recording
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    PROMPT_LIMIT=1

    # once gesture is acknowledged
    # start to listen for the voice command before starting recording
    for j in range(PROMPT_LIMIT):
        print('Speak!')
        time.sleep(0.5)
        guess = recognize_speech_from_mic(recognizer, microphone)
        if guess["transcription"]:
            break
        if not guess["success"]:
            break
        print("I didn't catch that. What did you say?\n")

        if guess["error"]:
            print("ERROR: {}".format(guess["error"]))
            break

    # debug statement
    print("You said: {}".format(guess["transcription"]))

    # start recording voice command
    if str(guess["transcription"]).find("start recording") != -1:
        time.sleep(2)
        print('Recording...')

        #save audio message as .wav file
        audio_file="message.wav"
        record_msg(recognizer, microphone, audio_file)

        # transcribe the audio message + save into a file
        transcribe(recognizer, microphone, audio_file)
