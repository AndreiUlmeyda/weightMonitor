from pydub import AudioSegment
from pydub.playback import play
from time import sleep
import logging


class AudioFeedback():
    def __init__(self):
        try:
            self.sound_start = AudioSegment.from_mp3("data/start.mp3") + 25
            self.sound_in_progress = AudioSegment.from_mp3("data/in_progress.mp3")
            self.sound_success = AudioSegment.from_mp3("data/success.mp3")
            self.sound_error = AudioSegment.from_mp3("data/error.mp3") - 10
        except FileNotFoundError:
            logging.error(
                'This program provides audio feedback using the files: \n\
start.mp3 \nin_progress.mp3 \nsuccess.mp3 \nerror.mp3 \n\
One or more of those appear to be missing.\n\
Please place respective files of appropriate content in your program directory.'
            )

    def start(self):
        play(self.sound_start)

    def in_progress(self, delay=0):
        sleep(delay)
        play(self.sound_in_progress)

    def success(self):
        play(self.sound_success)

    def error(self):
        play(self.sound_error)
