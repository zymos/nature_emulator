#!/usr/bin/env python
import pygame
# from pygame import mixer
import time
import threading
import sys

##########################################################
# Configure
#

def configure():
    ##########################
    # Global Vars
    global audio_transition_time, start_time_sec, stop_time_sec, stopwatch_count, stopwatch_interval, main_fade_time, debug, start_time, stop_time, BACKGROUND_SOUND_FILENAME, BACKGROUND_SOUND_VOLUME, BACKGROUND_SOUND_ENABLE


    BACKGROUND_SOUND_FILENAME = '/home/zymos/Documents/docs/projects/pi/nature_emulator/13_Streamside_Songbirds.ogg'
    BACKGROUND_SOUND_VOLUME = 0.7
    BACKGROUND_SOUND_ENABLE = True

    audio_transition_time = 2000 # time for audio crossfade (ms)
    # init_start_time_sec = 1
    start_time = "03:37" # HH:MM
    stop_time = "03:44" # HH:MM
    
    start_time_sec = 6 * 60 *60 # (s)
    stop_time_sec = 6 * 60 * 60 + 60 # (s)
    stopwatch_count = 0
    stopwatch_interval = 2 # (s)
    main_fade_time = 20 # (s)

    debug = True
    # debug = False
    # init_time = round(time.time()) # (s)
    # print init_time
    return




#############################################################
# Code
#


# Initialize modules
def initialize():
    # initialize modules
    pygame.mixer.init()
    pygame.mixer.pre_init(44100, -16, 2, 2048)
    pygame.init()
    print "%s: Audio module initialized..." % (time.strftime("%H:%M:%S"))
    return


# Plays a constant background sound, in an infinite loop
def play_background_sound():
    if BACKGROUND_SOUND_ENABLE:
        print "%s: Playing background sound" % (time.strftime("%H:%M:%S"))   
        pygame.mixer.music.load(BACKGROUND_SOUND_FILENAME)
        pygame.mixer.music.set_volume(BACKGROUND_SOUND_VOLUME)
        pygame.mixer.music.play(-1)

    return



# Main Function
def main():
    # main function

    print "\n\n\n"
    
    # CONFIGURE
    print "%s: Configuring..." % (time.strftime("%H:%M:%S"))
    configure()

    # print "  > start_time_sec = %ds; stop_time_sec = %ds; play_durration = %ds;" % (start_time_sec, stop_time_sec, (stop_time_sec - start_time_sec) )
    # print "  > main_fade_in_time = %ds;transition_time = %dms; stopwatch_interval = %ds;" % (main_fade_time, audio_transition_time, stopwatch_interval)
    
    # INTIALIZE
    initialize() # initialize modules


    #PLAY
    play_background_sound()
    
    while True:
        time.sleep(60)
        print "."
    # EXIT
    time.sleep(3)
    print
    print "%s: Shutting down modules..." % (time.strftime("%H:%M:%S"))
    pygame.quit()
    print "%s: Exiting...\n\n"% (time.strftime("%H:%M:%S"))
    return



if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, SystemExit):
        print
        print "%s: Shutting down modules..." % (time.strftime("%H:%M:%S"))
        pygame.quit()
        print "%s: Exiting...\n\n"% (time.strftime("%H:%M:%S"))
        sys.exit(1)

