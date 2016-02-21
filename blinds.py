import RPi.GPIO as GPIO
import time
import sys
import os


class Blinds:
    BOARD_SLEEP_TIME = 0.06
    PIN_CHANNEL = 3
    PIN_DOWN = 5
    PIN_MY = 7
    PIN_UP = 8

    def __init__(self, channel_file):
        self._channel_file = channel_file
        self._last_trigger = None

        GPIO.setmode(GPIO.BOARD)

        GPIO.setup(self.PIN_CHANNEL, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(self.PIN_DOWN, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(self.PIN_MY, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(self.PIN_UP, GPIO.OUT, initial=GPIO.HIGH)

        try:
            with open(channel_file, 'r') as f:
                self.channel = int(f.readline())
        except FileNotFoundError:
            self._save_channel(0)
        except ValueError:
            sys.stderr.write('Invalid content in channel file')

    def _sleep(self):
        time.sleep(self.BOARD_SLEEP_TIME)

    def _save_channel(self, channel):
        self.channel = channel
        with open(self._channel_file, 'w') as f:
            f.write(str(self.channel))
            os.fsync(f)        

    def _trigger(self, channel):
        GPIO.output(channel, GPIO.LOW)
        self._sleep()
        GPIO.output(channel, GPIO.HIGH)
        self._sleep()

    def set_channel(self, final):
        if self.channel == final:
            return

        # if last changed before less than 5 seconds, do not trigger extra click
        extra = 1
        if self._last_trigger is not None:
            diff = time.perf_counter() - self._last_trigger
            if diff < 5:
                extra = 0

        trigger_count = ((final+5) - self.channel) % 5
        for i in range(trigger_count + extra):
            self._trigger(self.PIN_CHANNEL)

        self._last_trigger = time.perf_counter()

        self._save_channel(final)

    def trigger_down(self):
        self._trigger(self.PIN_DOWN)
    
    def trigger_up(self):
        self._trigger(self.PIN_UP)

    def trigger_my(self):
        self._trigger(self.PIN_MY)

    @classmethod
    def cleanup(cls):
        GPIO.cleanup()

