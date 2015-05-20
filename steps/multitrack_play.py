#!/usr/bin/env python
import pygame
from time import sleep

pygame.mixer.init()
pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.init()
print "hey I finaly got this working!"
sounda= pygame.mixer.Sound('/home/zymos/Documents/docs/projects/pi/nature_emulator/tone01.wav')
soundb= pygame.mixer.Sound('/home/zymos/Documents/docs/projects/pi/nature_emulator/271.ogg')
soundc= pygame.mixer.Sound('/home/zymos/Documents/docs/projects/pi/nature_emulator/271.ogg')
soundd= pygame.mixer.Sound('/home/zymos/Documents/docs/projects/pi/nature_emulator/271.ogg')

print "one"
print sounda.get_length()
sounda.play(loops=0, maxtime=0, fade_ms=5000)
sleep(3)
sounda.fadeout(4000)
sleep(1)
print "two"
soundb.play()
sleep(1)
print "three"
soundc.play()
sleep(1)
print "four"
soundd.play()

sleep(7)
