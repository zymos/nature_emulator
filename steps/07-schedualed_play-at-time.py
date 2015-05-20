#!/usr/bin/env python
import pygame
import time 
import threading

def play_audio(filename, start_time_s, stop_time_s):

    durration_s = stop_time_s - start_time_s

    print "playing sound"
    sounda= pygame.mixer.Sound(filename)
    print "play 1"
    sounda.play(loops=0, maxtime=0, fade_ms=5000)
    time.sleep(durration_s)
    sounda.fadeout(5000)
    
    return

# Converts HH:MM:SS to seconds
def hms_to_seconds(t):
    h, m, s = [int(i) for i in t.split(':')]
    return 3600*h + 60*m + s

# Converts HH:MM to seconds
def hm_to_seconds(t):
    h, m = [int(i) for i in t.split(':')]
    return 3600*h + 60*m


def hello(a, b, c):
    print "a=%s, b=%s, c=%s" % (a, b, c)
    return


# Play file at start_time and stop at stop_time in a seperate thread
# start_time and stop_time is in HH:MM format
def schedual_play(filename, start_time_hm, stop_time_hm):
    
    stop_time_s = hm_to_seconds(stop_time_hm) #(seconds)
    start_time_s = hm_to_seconds(start_time_hm) #(seconds)
    current_time_hm = time.strftime("%H:%M")
    current_time_s = hm_to_seconds(current_time_hm) #(seconds)

    print "%s: Current_time: %s [%ds]" % (time.strftime("%H:%M:%S"), current_time_hm, current_time_s)
    print "%s: Start_time: %s [%ds]" % (time.strftime("%H:%M:%S"), start_time_hm, start_time_s)
    print "%s: Stop_time: %s [%ds]" % (time.strftime("%H:%M:%S"), stop_time_hm, stop_time_s)
    print "%s: Wait_time: [%ds]" % (time.strftime("%H:%M:%S"), start_time_s - current_time_s)
    if start_time_s - current_time_s < 0:
        print "%s: Warning wait_time is negative!: [%ds]" % (time.strftime("%H:%M:%S"), start_time_s - current_time_s)
    print "%s: Durration: [%ds]" % (time.strftime("%H:%M:%S"), stop_time_s - start_time_s)
    if stop_time_s - start_time_s < 0:
        print "%s: Warning durration is negative!: [%ds]" % (time.strftime("%H:%M:%S"), stop_time_s - start_time_s)

    print "%s: queing" % (time.strftime("%H:%M:%S"))

    # event2 = threading.Timer(2, hello, ["a", "b", "c"])
    # event2.daemon = True
    # event2.start()



    event = threading.Timer(start_time_s - current_time_s, play_audio, [filename, start_time_s, stop_time_s])
    event.daemon = True
    event.start()

    return



pygame.mixer.init()
pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.init()
print "Running Prog"

filename = '/home/zymos/Documents/docs/projects/pi/nature_emulator/250Hz_44100Hz_16bit_30sec.ogg'

start_time = "22:45"
stop_time = "22:46"

# print "playing sound"
# sound= pygame.mixer.Sound(filename)
# print "play 1"
# sound.play(loops=0, maxtime=0, fade_ms=5000)
# time.sleep(5)
# sound.fadeout(5000)



schedual_play(filename, start_time, stop_time)

# event1 = threading.Timer(5, play_audio, [filename])
# event1.start()
print "1s"
time.sleep(1)
print "2s"

time.sleep(1)
print "3s"

time.sleep(1)
print "4s"

time.sleep(1)
print "5s"

time.sleep(1)
print "6s"

time.sleep(1)
print "7s"

time.sleep(1)
print "8s"

time.sleep(1)
print "9s"

time.sleep(1)
print "10s"

x=1
while True:
    print "%s: sleeping for : 1m [%d]" % (time.strftime("%H:%M:%S"), x)
    time.sleep(60)
    x += 1


# soundb= pygame.mixer.Sound('/home/zymos/Documents/docs/projects/pi/nature_emulator/271.ogg')
# soundc= pygame.mixer.Sound('/home/zymos/Documents/docs/projects/pi/nature_emulator/271.ogg')
# soundd= pygame.mixer.Sound('/home/zymos/Documents/docs/projects/pi/nature_emulator/271.ogg')

# print "one"
# leep(1)
# print "two"
# soundb.play()
# time.sleep(1)
# print "three"
# soundc.play()
# time.sleep(1)
# print "four"
# soundd.play()

time.sleep(7)
