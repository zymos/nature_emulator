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
    global AUDIO_CROSSFADE_TIME, start_time_sec, stop_time_sec, STOPWATCH_INTERVAL, AUDIO_FADE_TIME, DEBUG, start_time, stop_time, BACKGROUND_SOUND_FILENAME, BACKGROUND_SOUND_VOLUME, BACKGROUND_SOUND_ENABLE

    # Background sound
    BACKGROUND_SOUND_ENABLE = True
    BACKGROUND_SOUND_FILENAME = '/home/zymos/Documents/docs/projects/pi/nature_emulator/13_Streamside_Songbirds.ogg'
    BACKGROUND_SOUND_VOLUME = 0.7

    # Location
    CITY_LOCATION = "Denver"


    # Modes

    FIXED_TIME_MODE_ENABLED = True
    START_OF_THE_DAY_MODE = "fixed" # options "fixed", "dawn", "sunrise"

    # Optional Configs
    AUDIO_CROSSFADE_TIME = 2000 # time for audio crossfade (ms)
    # init_start_time_sec = 1
    start_time = "13:36" # HH:MM
    stop_time = "14:32" # HH:MM
    
    start_time_sec = 6 * 60 *60 # (s)
    stop_time_sec = 6 * 60 * 60 + 60 # (s)
    STOPWATCH_INTERVAL = 2 # (s)
    AUDIO_FADE_TIME = 20 # (s)

    DEBUG = True
    # DEBUG = False
    # init_time = round(time.time()) # (s)
    # print init_time
    return




#############################################################
# Code
#




def audio_play_loop(filename, start_time_sec, stop_time_sec):
    # repeat playing a single file for a set durreation with crossfade
    # between

    # play_durration: total time file should be played (s)
    # global AUDIO_CROSSFADE_TIME # crossfade (ms)
    # global stopwatch_count
    # global STOPWATCH_INTERVAL # (s)
    # global init_time # (s)
    
    play_durration = stop_time_sec - start_time_sec # (s)
    print "%s: Starting Audio PlayerAudio, interval [%ds]" % (time.strftime("%H:%M:%S"), play_durration)
    print "%s: Loading sound file..." % (time.strftime("%H:%M:%S"))
    # trans = AUDIO_CROSSFADE_TIME
    sound = pygame.mixer.Sound(filename)
    file_length = sound.get_length() # file length (s)
    print "%s: Loaded sound file [%ds]" % (time.strftime("%H:%M:%S"), file_length//60)
       
    # Calculate how many play loops
    if file_length >= play_durration:
        play_loops=0
    else:
        if play_durration % file_length == 0:
            # perfect division
            play_loops = play_durration // file_length;
        else:
            # has remaining time
            play_loops =  (play_durration // file_length) + 1;


    # calculate sleep time
    sleep_time = play_durration - AUDIO_FADE_TIME

    if DEBUG:
        print "\t>>play_durration [%ds]" % (play_durration)
        print "\t>>file_length [%ds]" % (file_length)
        print "\t>>loops [%ds]" % (play_loops)
        print "\t>>Operation: play(%dx) > sleep [%ds] > fadeout > sleep [%ds] > return" % (play_loops, sleep_time, AUDIO_FADE_TIME)      

    
    # Playing
    sound.play(loops=int(play_loops), fade_ms=int(AUDIO_FADE_TIME*1000))
    time.sleep(sleep_time)
    sound.fadeout(AUDIO_FADE_TIME*1000)
    time.sleep(AUDIO_FADE_TIME)

    return




def stopwatch(start_time_sec, stop_time_sec):
    # sets a global minute counter
    global stopwatch_count
    # global STOPWATCH_INTERVAL # (s)
    # global init_time # (s)
    # durration (s)
    durration = stop_time_sec - start_time_sec

    stopwatch_count = 0
    durration_minutes = durration / 60 # s to m

    print "%s: Stopwatch started (max time = %dm)..." % (time.strftime("%H:%M:%S"), durration_minutes)
    # max_count = durration_minutes * 6
    max_count = durration / STOPWATCH_INTERVAL
    # print "max_count=", max_count
    while stopwatch_count < max_count:
        time.sleep(STOPWATCH_INTERVAL)
        stopwatch_count += 1
        #         # print "%s: Stopwatch: #%d - %ds" % (time.strftime("%H:%M:%S"), stopwatch_count, STOPWATCH_INTERVAL * stopwatch_count)
    return




# def play_timer(filename, start_time_sec, stop_time_sec):
    # time to play
    # global init_time # (s)
    
    # debgugging code
    # if DEBUG:
        # print "%s: Main function started... \n" % (time.strftime("%H:%M:%S"))
    
    # play_durration = stop_time_sec - start_time_sec
    # continious_play_for_set_durration(filename, start_time_sec, stop_time_sec)
    # return



# Initialize modules
def initialize():
    # initialize modules
    pygame.mixer.init()
    pygame.mixer.pre_init(44100, -16, 2, 2048)
    pygame.init()
    print "%s: Audio module initialized..." % (time.strftime("%H:%M:%S"))
    return



# def schedual_play():
    # time_delay = 1
    # play_event = threading.Timer(time_delay , play_timer, args=[filename, start_time_sec, stop_time_sec])
    # play_event.start()

    # return

def schedual_play(filename, start_time_hm, stop_time_hm):
    
    stop_time_s = hm_to_seconds(stop_time_hm) #(seconds)
    start_time_s = hm_to_seconds(start_time_hm) #(seconds)
    current_time_hm = time.strftime("%H:%M") # HH:MM
    current_time_s = hm_to_seconds(current_time_hm) #(seconds)
    durration_s = stop_time_s - start_time_s #(seconds)
    wait_time_s = start_time_s - current_time_s #(seconds)

    if DEBUG:
        print "%s: >>Current_time: %s [%ds]" % (time.strftime("%H:%M:%S"), current_time_hm, current_time_s)
        print "\t>>Start_time: %s [%ds]" % (start_time_hm, start_time_s)
        print "\t>>Stop_time: %s [%ds]" % (stop_time_hm, stop_time_s)
        print "\t>>Wait_time: [%ds]" % (start_time_s - current_time_s)
        if start_time_s - current_time_s < 0:
            print "\t>>Warning wait_time is negative!: [%ds]" % (start_time_s - current_time_s)
        print "\t>>Durration: [%ds]" % (stop_time_s - start_time_s)
        if stop_time_s - start_time_s < 0:
            print "\t>>Warning durration is negative!: [%ds]" % (stop_time_s - start_time_s)

    print "%s: Scheduling play @ %s [%ds]" % (time.strftime("%H:%M:%S"), start_time_hm, durration_s)

    if DEBUG:
        print "\t>>Opening play thread in [%ds], durration=%ds" % (wait_time_s, durration_s)


    # Play function
    # continious_play_for_set_durration(filename, start_time_sec, stop_time_sec)
    # event = threading.Timer(wait_time_s, continious_play_for_set_durration, [filename, start_time_s, stop_time_s])
    event = threading.Timer(wait_time_s, audio_play_loop, [filename, start_time_s, stop_time_s])
    event.daemon = True
    event.start()

    return



# Converts HH:MM:SS to seconds
def hms_to_seconds(t):
    h, m, s = [int(i) for i in t.split(':')]
    return 3600*h + 60*m + s



# Converts HH:MM:SS to seconds
def hm_to_seconds(t):
    h, m = [int(i) for i in t.split(':')]
    return 3600*h + 60*m 




# Main Function
def main():
    # main function

    print "\n\n\n"
    
    # CONFIGURE
    print "%s: Configuring..." % (time.strftime("%H:%M:%S"))
    configure()

    # print "  > start_time_sec = %ds; stop_time_sec = %ds; play_durration = %ds;" % (start_time_sec, stop_time_sec, (stop_time_sec - start_time_sec) )
    # print "  > main_fade_in_time = %ds;transition_time = %dms; STOPWATCH_INTERVAL = %ds;" % (AUDIO_FADE_TIME, AUDIO_CROSSFADE_TIME, STOPWATCH_INTERVAL)
    
    # INTIALIZE
    initialize() # initialize modules


    #PLAY
    # filename = '/home/zymos/Documents/docs/projects/pi/nature_emulator/250Hz_44100Hz_16bit_30sec.ogg'
    filename = '/home/zymos/Documents/docs/projects/pi/nature_emulator/13_Streamside_Songbirds.ogg'
    # continious_play_for_set_durration(filename, total_play_time)
    # play_timer(filename, start_time_sec, stop_time_sec)
    
    if DEBUG:
        print "%s: >>starting schedual_play function" % (time.strftime("%H:%M:%S"))
        print "\t>>file=%s" % (filename)
        print "\t>>start_time=%s, stop_time=%s" % (start_time, stop_time)


    schedual_play(filename, start_time, stop_time)
    # schedual_play()
    
    
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

