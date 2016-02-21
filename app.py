import RPi.GPIO as GPIO
import time

BOARD_SLEEP_TIME = 0.06

PIN_CHANNEL = 3
PIN_DOWN = 5
PIN_MY = 7
PIN_UP = 8

def sleep():
    time.sleep(BOARD_SLEEP_TIME)

def trigger(channel):
    GPIO.output(channel, GPIO.LOW)
    sleep()
    GPIO.output(channel, GPIO.HIGH)
    sleep()

def set_channel(current, final):
    if current == final:
        return

    trigger_count = ((final+5) - current) % 5
    for i in range(trigger_count + 1):
        trigger(PIN_CHANNEL)

try:
    GPIO.setmode(GPIO.BOARD)

    GPIO.setup(PIN_CHANNEL, GPIO.OUT, initial=GPIO.HIGH)
    GPIO.setup(PIN_DOWN, GPIO.OUT, initial=GPIO.HIGH)
    GPIO.setup(PIN_MY, GPIO.OUT, initial=GPIO.HIGH)
    GPIO.setup(PIN_UP, GPIO.OUT, initial=GPIO.HIGH)


    set_channel(4, 3)
finally:
    GPIO.cleanup()
