"""
This module provides audio feedback to indicate different stages of processing.
"""
from time import sleep
import logging
from pydub.playback import play
from pydub import AudioSegment


class AudioFeedback:
    """
    AudioFeedback is used to load sound files on startup and provide an interface
    to play sounds indicating different stages of the process.
    """
    def __init__(self):
        try:
            self.sound_start = AudioSegment.from_mp3("data/start.mp3") + 25
            self.sound_in_progress = AudioSegment.from_mp3(
                "data/in_progress.mp3")
            self.sound_success = AudioSegment.from_mp3("data/success.mp3")
            self.sound_error = AudioSegment.from_mp3("data/error.mp3") - 10
        except FileNotFoundError:
            logging.error(
                'This program provides audio feedback using the files: \n\
start.mp3 \nin_progress.mp3 \nsuccess.mp3 \nerror.mp3 \n\
One or more of those appear to be missing.\n\
Please place respective files of appropriate content in the \'data\' directory.'
            )

    def start(self):
        """
        Indicate the start of the process.
        """
        play(self.sound_start)

    def in_progress(self, delay=0):
        """
        Indicate an ongoing process. This should be called concurrently so that
        progress is actually happening during playback of the sound.
        """
        sleep(delay)
        play(self.sound_in_progress)

    def success(self):
        """
        Indicate that the process finished successfully.
        """
        play(self.sound_success)

    def error(self):
        """
        Indicate that the process finished with an error.
        """
        play(self.sound_error)
