#!/usr/bin/env python
import pygame
from time import sleep
import threading

def play_audio(file_name):
    print "playing sound"
    sounda= pygame.mixer.Sound(file_name)
    print "play 1"
    sounda.play(loops=0, maxtime=0)
    sleep(0.5)
    print "play 1"
    sounda.play(loops=0, maxtime=0)
    sleep(0.5)
    print "play 1"
    sounda.play(loops=0, maxtime=0)
    sleep(0.5)
    sounda= pygame.mixer.Sound(file_name)
    print "play 1"
    sounda.play(loops=0, maxtime=0)
    sleep(0.5)
    print "play 1"
    sounda.play(loops=0, maxtime=0)
    sleep(0.5)
    print "play 1"
    sounda.play(loops=0, maxtime=0)
    sleep(0.5)
    return

pygame.mixer.init()
pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.init()
print "Running Prog"

filename = '/home/zymos/Documents/docs/projects/pi/nature_emulator/blackbird.wav'
event1 = threading.Timer(5, play_audio, [filename])
event1.start()

sleep(1)
# pygame.time.wait(1000)
print "1"
sleep(1)
print "2"

sleep(1)
print "3"

sleep(1)
print "4"

sleep(1)
print "5"

sleep(1)
print "6"

sleep(1)
print "7"

sleep(1)
print "8"

sleep(1)
print "9"

sleep(1)
print "10"

sleep(1)
print "11"

# soundb= pygame.mixer.Sound('/home/zymos/Documents/docs/projects/pi/nature_emulator/271.ogg')
# soundc= pygame.mixer.Sound('/home/zymos/Documents/docs/projects/pi/nature_emulator/271.ogg')
# soundd= pygame.mixer.Sound('/home/zymos/Documents/docs/projects/pi/nature_emulator/271.ogg')

# print "one"
# leep(1)
# print "two"
# soundb.play()
# sleep(1)
# print "three"
# soundc.play()
# sleep(1)
# print "four"
# soundd.play()

sleep(7)
