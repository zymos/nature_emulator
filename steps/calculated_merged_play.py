#!/usr/bin/env python
import pygame
from time import sleep
import threading

def play_audio(filename, length):
    print "playing sound"
    global audio_transition_time

    sound= pygame.mixer.Sound(filename)
    fade_time = audio_transition_time
    sound.play(loops=0, maxtime=0, fade_ms=fade_time)
    sleep(length / 1000)
    sound.fadeout(fade_time)
    return

def continious_play_for_set_durration(filename, play_durration):
    # repeat playing a single file for a set durreation with crossfade
    # between
    global audio_transition_time
    trans = audio_transition_time
    # sound= pygame.mixer.Sound(filename)
    length = 9450 # sound.get_length()
    # pygame.mixer.quit()

    fudge = 1
    time = 0 #seconds
    n = 0
    while( time + trans < play_durration - fudge ):
        if (n+1) * (length - trans )> play_durration:
            cutoff = play_durration - time
            play_audio(filename, cutoff)
        else:
            play_audio(filename, length)
        n += 1
        time = n * ( length - trans )
    return

##########################
# Vars
# 
audio_transition_time = 2 * 1000 # time for audio crossfade (seconds)
init_start_time = 1
total_play_time = 2 * 60 * 1000 # play time needed (seconds)

pygame.mixer.init()
pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.init()
print "Running Prog"

filename = '/home/zymos/Documents/docs/projects/pi/nature_emulator/bird.ogg'
continious_play_for_set_durration(filename, total_play_time)


sleep(7)
