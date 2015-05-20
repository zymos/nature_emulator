#!/usr/bin/env python
import pygame
# from pygame import mixer
import time
import threading
import sys




def play_audio(sound, start_time, stop_time, length):
    global audio_transition_time # ms
    global stopwatch_count # count * interval = stopwatch time 
    global stopwatch_interval # (s)
    global main_fade_time # (s)
    global init_time # (s)
    # length: playtime length (s)

    fudge_factor = 1 # crossfade isn't exactly audo_transition_time
    # sound = pygame.mixer.Sound(filename) # load file
    # print "Loading file: ", filename
    new_length = length - audio_transition_time/1000 - fudge_factor # 

    # Start Volume at 0
    if stopwatch_count < 1: # start with volume=0
        volume = 0
        sound.set_volume(volume)
    
    # print "playing start..."
    # Start playing
    sound.play(loops=0, maxtime=0, fade_ms=audio_transition_time) #play
    print "%s: Playing audio clip time(%ds to %ds) interval[%ds of %ds] crossfade(%ds)..." % (time.strftime("%H:%M:%S"), stopwatch_count*stopwatch_interval, stopwatch_count*stopwatch_interval+length, length, stop_time-start_time, audio_transition_time/1000)
    # print "played"
    # sleep until play is over, and generates main fade

    # print "    stopwatch_interval=%d; stopwatch_count=%d; main_fade_time=%d" % (stopwatch_interval, stopwatch_count, main_fade_time)


    # Setting the volume(fade in/out) and sleeping until play is stopped
    if stopwatch_count * stopwatch_interval > stop_time - start_time - main_fade_time:
        # Fading Out
        print "%s: Volume: Fading out..." % (time.strftime("%H:%M:%S"))
    elif stopwatch_count * stopwatch_interval >= main_fade_time : 
        print "%s: Volume: Full..." % (time.strftime("%H:%M:%S"))
        # Normal (Full) Volume
        # print "    Full Volume"
        sound.set_volume(1)
        time.sleep(new_length)
    else: 
        # Fading In
        print "%s: Volume: Fading in..." % (time.strftime("%H:%M:%S"))
        time_left = new_length
        volume = 0
        while time_left > 0: # Main Fade
            # increment main fade in volume increase ever stopwatch 
            # interval until time is up
            # print"  Volume=%f play%d%d]", % (volume, time_left, new_length, (stopwatch_interval*stopwatch_count), main_fade_time)
            if stopwatch_count * stopwatch_interval < main_fade_time:
                time.sleep(stopwatch_interval)
                time_left -= stopwatch_interval
                volume = 1.0 * stopwatch_count * stopwatch_interval / main_fade_time
                print "%s: Fade-In: Volume increased to: %d%%" % (time.strftime("%H:%M:%S"), volume*100) 
                print "%s: Playing at full volume" % (time.strftime("%H:%M:%S")) 

            else:
                volume = 1.0
                time.sleep(time_left)
                time_left = 0

            # print"  Volume=%f play[%d of %d] fade[%d of %d]" % (volume, time_left, new_length, (stopwatch_interval*stopwatch_count), main_fade_time)
            sound.set_volume(volume)

    # time.sleep( new_length )
    sound.fadeout(audio_transition_time)
    print "%s: Play crossfading out (%ds)" % (time.strftime("%H:%M:%S"), audio_transition_time) 

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
    print "%s: Loading sound file..." % (time.strftime("%H:%M:%S"))
    trans = audio_transition_time
    sound = pygame.mixer.Sound(filename)
    length = sound.get_length() # file length (s)
    print "%s: Loaded sound file..." % (time.strftime("%H:%M:%S"))
   
    t = threading.Thread(target=stopwatch, args=[start_time, stop_time])
    t.setDaemon(True)
    t.start() 
    print "%s: Queue started..." % (time.strftime("%H:%M:%S"))
    print "  Audiofile length: %dm; Sound interval length: %dm" % (length//60, play_durration//60)
    
    # fudge = 1
    # time = 0 #seconds
    # n = 0
    
    play_count = play_durration // (length - audio_transition_time/1000)
    playtime_leftover = play_durration - (play_count * (length - audio_transition_time/1000))

    # print "    > file_length=%d; trans_time=%d; play_durration=%d" % (length, audio_transition_time, play_durration)
    # print "    > play_count=%d; playtime_leftover=%d" % (play_count, playtime_leftover)


    
    if length > play_durration: 
        #file length is longer that play durration
        print "%s: Queue: File longer than interval, queuing single truncated instance" % (time.strftime("%H:%M:%S"))
        print "    Queue: playing [1 of 1] %ds" % (play_durration)
        play_audio(sound, start_time, stop_time, play_durration)
    else: 
        # file length shorter than play durration, played more than once
        x = 0
        print "%s: Queue: File length shorter than play interval, playing multiple instances" % (time.strftime("%H:%M:%S"))
        while x < play_count:
            print "    Queue: playing #[%d of %d], [%d of %d] seconds" % (x+1, play_count+1, length, play_durration)
            play_audio(sound, start_time, stop_time, length)
            x += 1
        if playtime_leftover != 0: # play leftover time on play durration
            print "%s: Queue: playing last truncated instance, %ds" % (time.strftime("%H:%M:%S"), playtime_leftover)
            play_audio(sound, start_time, stop_time, playtime_leftover)

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

    print "%s: Stopwatch started (max time = %dm)...\n" % (time.strftime("%H:%M:%S"), durration_minutes)
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
    
    print "%s: Main function started... \n" % (time.strftime("%H:%M:%S"))
    # play_durration = stop_time - start_time
    continious_play_for_set_durration(filename, start_time, stop_time)

    


##########################
# Global Vars
# 
audio_transition_time = 2000 # time for audio crossfade (ms)
# init_start_time = 1
start_time = 6 * 60 *60 # (s)
stop_time = 6 * 60 * 60 + 600 # (s)
stopwatch_count = 0
stopwatch_interval = 2 # (s)
main_fade_time = 20 # (s)
init_time = round(time.time()) # (s)
# print init_time

try:
    print "\n\n\n"
    print "%s: Configuration..." % (time.strftime("%H:%M:%S"))
    # print "  > start_time = %ds; stop_time = %ds; play_durration = %ds;" % (start_time, stop_time, (stop_time - start_time) )
    # print "  > main_fade_in_time = %ds;transition_time = %dms; stopwatch_interval = %ds;" % (main_fade_time, audio_transition_time, stopwatch_interval)

    pygame.mixer.init()
    pygame.mixer.pre_init(44100, -16, 2, 2048)
    pygame.init()
    print "%s: Pygame initialized...\n" % (time.strftime("%H:%M:%S"))

    filename = '/home/zymos/Documents/docs/projects/pi/nature_emulator/250Hz_44100Hz_16bit_30sec.ogg'
    # filename = '/home/zymos/Documents/docs/projects/pi/nature_emulator/13_Streamside_Songbirds.ogg'
    # continious_play_for_set_durration(filename, total_play_time)
    play_timer(filename, start_time, stop_time)

    time.sleep(7)


except (KeyboardInterrupt, SystemExit):
    print
    print "Shutting down modules..."
    pygame.quit()
    print "Exiting...\n\n"
    sys.exit(1)
