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
    start_time = "03:37" # HH:MM
    stop_time = "03:44" # HH:MM
    
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

def play_audio(sound, start_time_sec, stop_time_sec, length, file_length):
    # global AUDIO_CROSSFADE_TIME # ms
    # global stopwatch_count # count * interval = stopwatch time 
    # global STOPWATCH_INTERVAL # (s)
    # global AUDIO_FADE_TIME # (s)
    # global init_time # (s)
    # length: playtime length (s)

    fudge_factor = 0 # crossfade isn't exactly audo_transition_time
    # sound = pygame.mixer.Sound(filename) # load file
    # print "Loading file: ", filename
    new_length = length - AUDIO_CROSSFADE_TIME/1000 - fudge_factor # 




    #dubugging code
    if DEBUG:
        print "%s: >>Playing audio clip [%ds]" % (time.strftime("%H:%M:%S"), new_length)
        print "\t>>time(%ds to %ds) interval[%ds of %ds] crossfade(%ds) "% (stopwatch_count*STOPWATCH_INTERVAL, stopwatch_count*STOPWATCH_INTERVAL+length, length, stop_time_sec-start_time_sec, AUDIO_CROSSFADE_TIME/1000)
        print "\t>>stopwatch_time=%ds; file_length=%ds; full_play_durration=%ds" % (stopwatch_count*STOPWATCH_INTERVAL, file_length, stop_time_sec-start_time_sec)
        print "\t>>stopwatch_time=%ds; clip_play_length=%ds; new_length=%ds" % (stopwatch_count*STOPWATCH_INTERVAL, length, new_length)
        print "\t>>stopwatch_time=%ds; AUDIO_FADE_TIME=%ds; transition_time=%ds" % (stopwatch_count*STOPWATCH_INTERVAL, AUDIO_FADE_TIME, AUDIO_CROSSFADE_TIME)

    # @ time=0; Start Volume at 0
    # if stopwatch_count < 1: # start with volume=0
        # volume = 0
        # sound.set_volume(volume)
    
    # Playing, with fade in/out
    if file_length > stop_time_sec - start_time_sec:
        # when file is longer than play duration
        if DEBUG: print "\t>>file is longer than play duration"        
        print "%s: Volume: Fade In [%ds]" % (time.strftime("%H:%M:%S"), AUDIO_FADE_TIME)
        sound.play(loops=0, maxtime=0, fade_ms=AUDIO_FADE_TIME*1000) #play
        time.sleep(length - AUDIO_FADE_TIME)
        print "%s: Volume: Fade Out [%ds]" % (time.strftime("%H:%M:%S"), AUDIO_FADE_TIME)
        sound.fadeout(AUDIO_FADE_TIME*1000)
        time.sleep(AUDIO_FADE_TIME)
    elif file_length >= AUDIO_FADE_TIME:
        # when file is long enough for a complete fade in/out
        # but file_length is less than the full play_durration
        if DEBUG: print "\t>>file_length < play duration, but still >AUDIO_FADE_TIME"
        if stopwatch_count < 2:
            # Initial: Fade In
            print "%s: Volume: Fade In [%ds]" % (time.strftime("%H:%M:%S"), AUDIO_FADE_TIME)            
            sound.play(loops=0, maxtime=0, fade_ms=AUDIO_FADE_TIME*1000) #play
            time.sleep(new_length)
            sound.fadeout(AUDIO_CROSSFADE_TIME)
        elif stopwatch_count * STOPWATCH_INTERVAL >= stop_time_sec - start_time_sec - AUDIO_FADE_TIME:
            # End: Fade Out
            # may make play longer than play_durration by AUDIO_FADE_TIME
            sound.play(loops=0, maxtime=0, fade_ms=AUDIO_CROSSFADE_TIME) #play
            time.sleep(length)
            sound.fadeout(AUDIO_FADE_TIME*1000)
            print "%s: Volume: Fade Out [added %ds to play time for fade]" % (time.strftime("%H:%M:%S"), AUDIO_FADE_TIME)           
            time.sleep(AUDIO_FADE_TIME)
        else:
            # Middle: no fade-in/out
            if DEBUG: print "\t>>playing clip in middle, no fade needed"
            sound.play(loops=0, maxtime=0, fade_ms=AUDIO_CROSSFADE_TIME) #play
            time.sleep(length)
            sound.fadeout(AUDIO_CROSSFADE_TIME)
    else:
        # when file is shorter than a complete fade, so it uses a 
        # incremental volume increase, not as smooth
        sound.play(loops=0, maxtime=0, fade_ms=AUDIO_CROSSFADE_TIME) #play
        time_count = 0
        while time_count <= new_length:
            # if stopwatch_count == 0:
                # print "%s: Volume: Fade In (%d%%)" % (time.strftime("%H:%M:%S"), volume*100)
                # sound.set_volume(0)
            if stopwatch_count * STOPWATCH_INTERVAL <= AUDIO_FADE_TIME:
                volume = 1.0 * stopwatch_count * STOPWATCH_INTERVAL / AUDIO_FADE_TIME
                sound.set_volume(volume)
                if volume == 0.1:
                    print "%s: Volume: Fade In" % (time.strftime("%H:%M:%S"))
                if DEBUG:
                    print "%s: >>Volume: Fade In (%d%%)" % (time.strftime("%H:%M:%S"), volume*100)
            elif stop_time_sec - start_time_sec - STOPWATCH_INTERVAL*stopwatch_count <= AUDIO_FADE_TIME:
                volume = (1.0 * stop_time_sec - start_time_sec - stopwatch_count * STOPWATCH_INTERVAL) / AUDIO_FADE_TIME
                sound.set_volume(volume)
                if volume == 0.9:
                    print "%s: Volume: Fade Out" % (time.strftime("%H:%M:%S"))
                if DEBUG:
                    print "%s: >>Volume: Fade Out (%d%%)" % (time.strftime("%H:%M:%S"), volume*100)
            else:
                volume = 1.0
                sound.set_volume(volume)
                if DEBUG:
                    print "%s: >>Volume: is full (%d%%)" % (time.strftime("%H:%M:%S"), volume*100)
            
            # Debuging code
            if DEBUG:
                print "\t>>time=%ds: interval_play_time=%ds"  % (stopwatch_count * STOPWATCH_INTERVAL, stop_time_sec - start_time_sec)
                print "\t>>time=%ds: stopwatch_count=%d; STOPWATCH_INTERVAL=%ds" % (stopwatch_count * STOPWATCH_INTERVAL, stopwatch_count, STOPWATCH_INTERVAL)
                print "\t>>time=%ds: clip_time=%ds; clip_length=%ds" % (stopwatch_count * STOPWATCH_INTERVAL, time_count, new_length)
                print "\t>>time=%ds: volume=%d" % (stopwatch_count * STOPWATCH_INTERVAL, volume)

            time_count += STOPWATCH_INTERVAL
            time.sleep(STOPWATCH_INTERVAL)
        sound.fadeout(AUDIO_CROSSFADE_TIME)

    if DEBUG:
        print "%s: >>Clip crossfading out (%dms)" % (time.strftime("%H:%M:%S"), AUDIO_CROSSFADE_TIME) 

    return




def continious_play_for_set_durration(filename, start_time_sec, stop_time_sec):
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
    trans = AUDIO_CROSSFADE_TIME
    sound = pygame.mixer.Sound(filename)
    file_length = sound.get_length() # file length (s)
    print "%s: Loaded sound file [%ds]" % (time.strftime("%H:%M:%S"), file_length//60)
   
    t = threading.Thread(target=stopwatch, args=[start_time_sec, stop_time_sec])
    t.setDaemon(True)
    t.start() 

    time.sleep(0.1) # ensure events are never exactly on stopwatch change


    
    #debuging
    if DEBUG:
        print "%s: >>Queue started..." % (time.strftime("%H:%M:%S"))
        print "\t>>Audio clip length: %dm; play interval: %dm" % (file_length//60, play_durration//60)
    
    # fudge = 1
    # time = 0 #seconds
    # n = 0
    
    play_count = play_durration // (file_length - AUDIO_CROSSFADE_TIME/1000)
    playtime_leftover = play_durration - (play_count * (file_length - AUDIO_CROSSFADE_TIME/1000))

    # print "    > file_length=%d; trans_time=%d; play_durration=%d" % (length, AUDIO_CROSSFADE_TIME, play_durration)
    # print "    > play_count=%d; playtime_leftover=%d" % (play_count, playtime_leftover)


    
    if file_length > play_durration: 
        #file length is longer that play durration
        print "%s: Queue: playing #[1 of 1] truncated to %ds" % (time.strftime("%H:%M:%S"), play_durration)
        play_audio(sound, start_time_sec, stop_time_sec, play_durration, file_length)
    else: 
        # file length shorter than play durration, played more than once
        x = 0
        # print "%s: Queue: playing #[%d of %d], %ds" % (time.strftime("%H:%M:%S"), x+1, play_count+1, length)
        while x < play_count:
            print "%s: Queue: playing #[%d of %d], %ds" % (time.strftime("%H:%M:%S"), x+1, play_count+1, file_length)
            play_audio(sound, start_time_sec, stop_time_sec, file_length, file_length)
            x += 1
        if playtime_leftover != 0: # play leftover time on play durration
            print "%s: Queue: playing #[%d of %d], truncated to %ds" % (time.strftime("%H:%M:%S"), x+1, play_count+1, playtime_leftover)
            play_audio(sound, start_time_sec, stop_time_sec, playtime_leftover, file_length)

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
        print "%s: >>Start_time: %s [%ds]" % (time.strftime("%H:%M:%S"), start_time_hm, start_time_s)
        print "%s: >>Stop_time: %s [%ds]" % (time.strftime("%H:%M:%S"), stop_time_hm, stop_time_s)
        print "%s: >>Wait_time: [%ds]" % (time.strftime("%H:%M:%S"), start_time_s - current_time_s)
        if start_time_s - current_time_s < 0:
            print "%s: >>Warning wait_time is negative!: [%ds]" % (time.strftime("%H:%M:%S"), start_time_s - current_time_s)
        print "%s: >>Durration: [%ds]" % (time.strftime("%H:%M:%S"), stop_time_s - start_time_s)
        if stop_time_s - start_time_s < 0:
            print "%s: >>Warning durration is negative!: [%ds]" % (time.strftime("%H:%M:%S"), stop_time_s - start_time_s)

    print "%s: Schedualing play @ %s [%ds]" % (time.strftime("%H:%M:%S"), start_time_hm, durration_s)

    if DEBUG:
        print "%s: >>Starting play thread, waiting=%ds, durration=%ds" % (time.strftime("%H:%M:%S"), wait_time_s, durration_s)


    # Play function
    # continious_play_for_set_durration(filename, start_time_sec, stop_time_sec)
    event = threading.Timer(wait_time_s, continious_play_for_set_durration, [filename, start_time_s, stop_time_s])
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
    filename = '/home/zymos/Documents/docs/projects/pi/nature_emulator/250Hz_44100Hz_16bit_30sec.ogg'
    # filename = '/home/zymos/Documents/docs/projects/pi/nature_emulator/13_Streamside_Songbirds.ogg'
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

