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
    global audio_transition_time, start_time, stop_time, stopwatch_count, stopwatch_interval, main_fade_time, debug

    audio_transition_time = 2000 # time for audio crossfade (ms)
    # init_start_time = 1
    start_time = 6 * 60 *60 # (s)
    stop_time = 6 * 60 * 60 + 60 # (s)
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

def play_audio(sound, start_time, stop_time, length, file_length):
    global audio_transition_time # ms
    global stopwatch_count # count * interval = stopwatch time 
    global stopwatch_interval # (s)
    global main_fade_time # (s)
    global init_time # (s)
    # length: playtime length (s)

    fudge_factor = 0 # crossfade isn't exactly audo_transition_time
    # sound = pygame.mixer.Sound(filename) # load file
    # print "Loading file: ", filename
    new_length = length - audio_transition_time/1000 - fudge_factor # 




    #dubugging code
    if debug:
        print "%s: Playing audio clip [%ds]" % (time.strftime("%H:%M:%S"), new_length)
        print "\t\ttime(%ds to %ds) interval[%ds of %ds] crossfade(%ds) "% (stopwatch_count*stopwatch_interval, stopwatch_count*stopwatch_interval+length, length, stop_time-start_time, audio_transition_time/1000)
        print "\t\tstopwatch_time=%ds; file_length=%ds; full_play_durration=%ds" % (stopwatch_count*stopwatch_interval, file_length, stop_time-start_time)
        print "\t\tstopwatch_time=%ds; clip_play_length=%ds; new_length=%ds" % (stopwatch_count*stopwatch_interval, length, new_length)
        print "\t\tstopwatch_time=%ds; main_fade_time=%ds; transition_time=%ds" % (stopwatch_count*stopwatch_interval, main_fade_time, audio_transition_time)

    # @ time=0; Start Volume at 0
    # if stopwatch_count < 1: # start with volume=0
        # volume = 0
        # sound.set_volume(volume)
    
    # Playing, with fade in/out
    if file_length > stop_time - start_time:
        # when file is longer than play duration
        if debug: print "\tfile is longer than play duration"        
        print "%s: Volume: Fade In [%ds]" % (time.strftime("%H:%M:%S"), main_fade_time)
        sound.play(loops=0, maxtime=0, fade_ms=main_fade_time*1000) #play
        time.sleep(length - main_fade_time)
        print "%s: Volume: Fade Out [%ds]" % (time.strftime("%H:%M:%S"), main_fade_time)
        sound.fadeout(main_fade_time*1000)
        time.sleep(main_fade_time)
    elif file_length >= main_fade_time:
        # when file is long enough for a complete fade in/out
        # but file_length is less than the full play_durration
        if debug: print "\tfile_length < play duration, but still >main_fade_time"
        if stopwatch_count < 2:
            # Initial: Fade In
            print "%s: Volume: Fade In [%ds]" % (time.strftime("%H:%M:%S"), main_fade_time)            
            sound.play(loops=0, maxtime=0, fade_ms=main_fade_time*1000) #play
            time.sleep(new_length)
            sound.fadeout(audio_transition_time)
        elif stopwatch_count * stopwatch_interval >= stop_time - start_time - main_fade_time:
            # End: Fade Out
            # may make play longer than play_durration by main_fade_time
            sound.play(loops=0, maxtime=0, fade_ms=audio_transition_time) #play
            time.sleep(length)
            sound.fadeout(main_fade_time*1000)
            print "%s: Volume: Fade Out [added %ds to play time for fade]" % (time.strftime("%H:%M:%S"), main_fade_time)           
            time.sleep(main_fade_time)
        else:
            # Middle: no fade-in/out
            if debug: print "\tplaying clip in middle, no fade needed"
            sound.play(loops=0, maxtime=0, fade_ms=audio_transition_time) #play
            time.sleep(length)
            sound.fadeout(audio_transition_time)
    else:
        # when file is shorter than a complete fade, so it uses a 
        # incremental volume increase, not as smooth
        sound.play(loops=0, maxtime=0, fade_ms=audio_transition_time) #play
        time_count = 0
        while time_count <= new_length:
            # if stopwatch_count == 0:
                # print "%s: Volume: Fade In (%d%%)" % (time.strftime("%H:%M:%S"), volume*100)
                # sound.set_volume(0)
            if stopwatch_count * stopwatch_interval <= main_fade_time:
                volume = 1.0 * stopwatch_count * stopwatch_interval / main_fade_time
                sound.set_volume(volume)
                if volume == 0.1:
                    print "%s: Volume: Fade In" % (time.strftime("%H:%M:%S"))
                if debug:
                    print "%s: Volume: Fade In (%d%%)" % (time.strftime("%H:%M:%S"), volume*100)
            elif stop_time - start_time - stopwatch_interval*stopwatch_count <= main_fade_time:
                volume = (1.0 * stop_time - start_time - stopwatch_count * stopwatch_interval) / main_fade_time
                sound.set_volume(volume)
                if volume == 0.9:
                    print "%s: Volume: Fade Out" % (time.strftime("%H:%M:%S"))
                if debug:
                    print "%s: Volume: Fade Out (%d%%)" % (time.strftime("%H:%M:%S"), volume*100)
            else:
                volume = 1.0
                sound.set_volume(volume)
                if debug:
                    print "%s: Volume: is full (%d%%)" % (time.strftime("%H:%M:%S"), volume*100)
            
            # Debuging code
            if debug:
                print "\t time=%ds: interval_play_time=%ds"  % (stopwatch_count * stopwatch_interval, stop_time - start_time)
                print "\t time=%ds: stopwatch_count=%d; stopwatch_interval=%ds" % (stopwatch_count * stopwatch_interval, stopwatch_count, stopwatch_interval)
                print "\t time=%ds: clip_time=%ds; clip_length=%ds" % (stopwatch_count * stopwatch_interval, time_count, new_length)
                print "\t time=%ds: volume=%d" % (stopwatch_count * stopwatch_interval, volume)

            time_count += stopwatch_interval
            time.sleep(stopwatch_interval)
        sound.fadeout(audio_transition_time)

    if debug:
        print "%s: Clip crossfading out (%dms)" % (time.strftime("%H:%M:%S"), audio_transition_time) 

    return




def continious_play_for_set_durration(filename, start_time, stop_time):
    # repeat playing a single file for a set durreation with crossfade
    # between

    # play_durration: total time file should be played (s)
    global audio_transition_time # crossfade (ms)
    global stopwatch_count
    global stopwatch_interval # (s)
    global init_time # (s)
    
    play_durration = stop_time - start_time # (s)
    print "%s: Audio play interval [%ds]" % (time.strftime("%H:%M:%S"), play_durration)
    print "%s: Loading sound file..." % (time.strftime("%H:%M:%S"))
    trans = audio_transition_time
    sound = pygame.mixer.Sound(filename)
    file_length = sound.get_length() # file length (s)
    print "%s: Loaded sound file [%ds]" % (time.strftime("%H:%M:%S"), file_length//60)
   
    t = threading.Thread(target=stopwatch, args=[start_time, stop_time])
    t.setDaemon(True)
    t.start() 

    time.sleep(0.1) # ensure events are never exactly on stopwatch change


    
    #debuging
    if debug:
        print "%s: Queue started..." % (time.strftime("%H:%M:%S"))
        print "    Audio clip length: %dm; play interval: %dm" % (file_length//60, play_durration//60)
    
    # fudge = 1
    # time = 0 #seconds
    # n = 0
    
    play_count = play_durration // (file_length - audio_transition_time/1000)
    playtime_leftover = play_durration - (play_count * (file_length - audio_transition_time/1000))

    # print "    > file_length=%d; trans_time=%d; play_durration=%d" % (length, audio_transition_time, play_durration)
    # print "    > play_count=%d; playtime_leftover=%d" % (play_count, playtime_leftover)


    
    if file_length > play_durration: 
        #file length is longer that play durration
        print "%s: Queue: playing #[1 of 1] truncated to %ds" % (time.strftime("%H:%M:%S"), play_durration)
        play_audio(sound, start_time, stop_time, play_durration, file_length)
    else: 
        # file length shorter than play durration, played more than once
        x = 0
        # print "%s: Queue: playing #[%d of %d], %ds" % (time.strftime("%H:%M:%S"), x+1, play_count+1, length)
        while x < play_count:
            print "%s: Queue: playing #[%d of %d], %ds" % (time.strftime("%H:%M:%S"), x+1, play_count+1, file_length)
            play_audio(sound, start_time, stop_time, file_length, file_length)
            x += 1
        if playtime_leftover != 0: # play leftover time on play durration
            print "%s: Queue: playing #[%d of %d], truncated to %ds" % (time.strftime("%H:%M:%S"), x+1, play_count+1, playtime_leftover)
            play_audio(sound, start_time, stop_time, playtime_leftover, file_length)

    return




def stopwatch(start_time, stop_time):
    # sets a global minute counter
    global stopwatch_count
    global stopwatch_interval # (s)
    global init_time # (s)
    # durration (s)
    durration = stop_time - start_time

    stopwatch_count = 0
    durration_minutes = durration / 60 # s to m

    print "%s: Stopwatch started (max time = %dm)..." % (time.strftime("%H:%M:%S"), durration_minutes)
    # max_count = durration_minutes * 6
    max_count = durration / stopwatch_interval
    # print "max_count=", max_count
    while stopwatch_count < max_count:
        time.sleep(stopwatch_interval)
        stopwatch_count += 1
        #         # print "%s: Stopwatch: #%d - %ds" % (time.strftime("%H:%M:%S"), stopwatch_count, stopwatch_interval * stopwatch_count)
    return




def play_timer(filename, start_time, stop_time):
    # time to play
    global init_time # (s)
    
    # debgugging code
    if debug:
        print "%s: Main function started... \n" % (time.strftime("%H:%M:%S"))
    
    # play_durration = stop_time - start_time
    continious_play_for_set_durration(filename, start_time, stop_time)
    return



def initialize():
    # initialize modules
    pygame.mixer.init()
    pygame.mixer.pre_init(44100, -16, 2, 2048)
    pygame.init()
    print "%s: Audio module initialized..." % (time.strftime("%H:%M:%S"))
    return




def main():
    # main function

    print "\n\n\n"
    
    # CONFIGURE
    print "%s: Configuring..." % (time.strftime("%H:%M:%S"))
    configure()

    # print "  > start_time = %ds; stop_time = %ds; play_durration = %ds;" % (start_time, stop_time, (stop_time - start_time) )
    # print "  > main_fade_in_time = %ds;transition_time = %dms; stopwatch_interval = %ds;" % (main_fade_time, audio_transition_time, stopwatch_interval)
    
    # INTIALIZE
    initialize() # initialize modules


    #PLAY
    filename = '/home/zymos/Documents/docs/projects/pi/nature_emulator/250Hz_44100Hz_16bit_30sec.ogg'
    # filename = '/home/zymos/Documents/docs/projects/pi/nature_emulator/13_Streamside_Songbirds.ogg'
    # continious_play_for_set_durration(filename, total_play_time)
    play_timer(filename, start_time, stop_time)

    
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

