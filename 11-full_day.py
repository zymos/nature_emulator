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
    global AUDIO_CROSSFADE_TIME, STOPWATCH_INTERVAL, AUDIO_FADE_TIME, DEBUG, BACKGROUND_SOUND_FILENAME, BACKGROUND_SOUND_VOLUME, BACKGROUND_SOUND_ENABLE, ENABLE_FIXED_TIME_MODE, START_OF_THE_DAY_MODE, END_OF_THE_DAY_MODE, ENABLE_FIXED_LATENIGHT, FIXED_TIME_DAWN, FIXED_TIME_SUNRISE, FIXED_TIME_MIDMORNING, FIXED_TIME_MIDAFTERNOON, FIXED_TIME_SUNSET, FIXED_TIME_DUSK, FIXED_TIME_LATENIGHT, DAWN_AUDIO_FILENAME, SUNRISE_AUDIO_FILENAME, MIDMORNING_AUDIO_FILENAME, MIDAFTERNOON_AUDIO_FILENAME, SUNSET_AUDIO_FILENAME, DUSK_AUDIO_FILENAME, LATENIGHT_AUDIO_FILENAME, CITY_LOCATION, AUDIO_DIRECTORY

    #######################
    # Main Configs
    
    AUDIO_DIRECTORY = ""
        # location of audio files: full path for directory

    CITY_LOCATION = "Denver"
        # see: 


    ####################
    # Background sound
    BACKGROUND_SOUND_ENABLE = True
        # Will play the following file 24h a day (True or False)
    BACKGROUND_SOUND_FILENAME = '13_Streamside_Songbirds.ogg'
        # recomended: rain, waves, wind
    BACKGROUND_SOUND_VOLUME = 0.7
        # Volume for the background sound (0.0 min - 1.0 max)

######################################
# Definition for times of the day
#
# Division of times of day
# Beginning of day>>
#   dawn > morning > midday > evening > dusk > night
# <<End of day
# 
# dawn: twilight till sunrise example(05:00 to 05:40)
#       twilight = sun 18 degrees below the horizon
#       sunrise = sunrise
# morning: sunrise till midmorning example(5:45 to 10:00)
#       sunrise = sunrise
#       midmorning = (12:00 - sunrise) / 2
# midday: midmorning till midafternoon example(10:00 to 15:00
#       midmorning = (12:00 - sunrise) / 2
#       midafternoon = (sunset - 12:00) / 2
# evening: midafternoon to sunset, example(15:00 to 20:15)
#       midafternoon: (sunset - 12:00) / 2
#       sunset = sunset
# dusk: sunset till dusk, example(20:15 to 20:45)
#       sunset = sunset
#       dusk =  sun 18 degrees below the horizon
# night: dusk till latenight, example(20:45 to 22:00)
#       dusk =  sun 18 degrees below the horizon
#       latenight = (24:00 - sunset) / 2
#
    # Fixed times of the day

    ###############################
    # Time of day Modes
    # 
    ENABLE_FIXED_TIME_MODE = True
        # if True "start_of_day" and "end_of_day" is set to "fixed"
        # True or False
    START_OF_THE_DAY_MODE = "fixed" # options "fixed", "dawn", "sunrise"
        # if start of day is "fixed", set "dawn" and "sunrise" times
    END_OF_THE_DAY_MODE = "fixed" 
        # options "fixed", "sunset", "dusk", "latenight"
        # if end of day is "fixed", set "dawn" and "sunrise" times
        # if sunset, audio will end at sunset
        # if dusk, audio will end at dusk
        # if latenight, audio will end a latenight
    ENABLE_FIXED_LATENIGHT = True
        # if mode is "fixed" this allows you to disable audio after dusk
        # True or False

    ##################################
    # Times of day for "fixed" mode
    # Time format: HH:MM in 24h clock, example 22:00 is 10pm
    FIXED_TIME_DAWN = "05:00"
    FIXED_TIME_SUNRISE = "05:45"
    FIXED_TIME_MIDMORNING = "10:00"
    FIXED_TIME_MIDAFTERNOON = "15:00"
    FIXED_TIME_SUNSET = "20:15"
    FIXED_TIME_DUSK = "20:45"
    FIXED_TIME_LATENIGHT = "22:00"

    #####################
    # Audio Filenames
    # mp3, wav or ogg files
    DAWN_AUDIO_FILENAME = '13_Streamside_Songbirds.ogg'
        # recomended: light bird sounds
    SUNRISE_AUDIO_FILENAME = '13_Streamside_Songbirds.ogg'
        # recomended: moderate bird sounds
    MIDMORNING_AUDIO_FILENAME = '13_Streamside_Songbirds.ogg'
        # recomended: light bird sounds
    MIDAFTERNOON_AUDIO_FILENAME = '13_Streamside_Songbirds.ogg'
        # recomended: moderate birds sounds, rain, storms
    SUNSET_AUDIO_FILENAME = '13_Streamside_Songbirds.ogg'
        # recomended: crickets, frogs, 
    DUSK_AUDIO_FILENAME = '13_Streamside_Songbirds.ogg'
        # recomended: crickets, frogs
    LATENIGHT_AUDIO_FILENAME = '13_Streamside_Songbirds.ogg'
        # recomended: owls, coyotes, wolves


    #########################
    # Optional
    #
    OVERLAP_TIME = 120 
        # overlap time between files, between times of day (seconds)

    AUDIO_FADE_TIME = 20 
        # fade in/out time for each audio file (seconds)

    DEBUG = True
        # DEBUG = False
                # enable more verbose output for debuging (True or False)


    # Old Configs
    AUDIO_CROSSFADE_TIME = 2000 # time for audio crossfade (ms)
    # init_start_time_sec = 1
    start_time = "13:36" # HH:MM
    stop_time = "14:32" # HH:MM
    


    # init_time = round(time.time()) # (s)
    # print init_time
    return




#############################################################
# Code
#


# Plays a constant background sound, in an infinite loop
def play_background_sound():
    if BACKGROUND_SOUND_ENABLE:
        print "%s: Playing background sound" % (time.strftime("%H:%M:%S"))   
        pygame.mixer.music.load(BACKGROUND_SOUND_FILENAME)
        pygame.mixer.music.set_volume(BACKGROUND_SOUND_VOLUME)
        pygame.mixer.music.play(-1)

    return


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



def generate_daily_schedule():
    time_now = time.strftime("%H:%M")

    print "%s: Generating scheduled events for the day [%s]" % (time.strftime("%H:%M:%S"), time.strftime("%a, %e %b %Y"))

    if DEBUG:
        print "\t>>The time is now [%s]" % (time_now)

    # Getting Events

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
    # configure()
    import config_file

    # print "  > start_time_sec = %ds; stop_time_sec = %ds; play_durration = %ds;" % (start_time_sec, stop_time_sec, (stop_time_sec - start_time_sec) )
    # print "  > main_fade_in_time = %ds;transition_time = %dms; STOPWATCH_INTERVAL = %ds;" % (AUDIO_FADE_TIME, AUDIO_CROSSFADE_TIME, STOPWATCH_INTERVAL)
    
    # INTIALIZE
    initialize() # initialize modules

    generate_daily_schedule()

    # Start background sound
    if BACKGROUND_SOUND_ENABLE:
        play_background_sound()
 
    
    #PLAY
    # filename = '/home/zymos/Documents/docs/projects/pi/nature_emulator/250Hz_44100Hz_16bit_30sec.ogg'
    # filename = '/home/zymos/Documents/docs/projects/pi/nature_emulator/13_Streamside_Songbirds.ogg'
    # continious_play_for_set_durration(filename, total_play_time)
    # play_timer(filename, start_time_sec, stop_time_sec)
    
    # if DEBUG:
        # print "%s: >>starting schedual_play function" % (time.strftime("%H:%M:%S"))
        # print "\t>>file=%s" % (filename)
        # print "\t>>start_time=%s, stop_time=%s" % (start_time, stop_time)


    # schedual_play(filename, start_time, stop_time)
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

