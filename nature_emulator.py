#!/usr/bin/env python2.7  

#########################################################################
#	Nature Emulator
#	Author: ZyMOS
#	Date: 16 April 2015
#	
#	Description: This  
#
#	Files:	nature_emulator-init.sh: 
#			init script runs python script
#		nature_emulator.py: 
#			python script that does the work
#
#       Requirements: pygame, pymad, astral, pytz
#
#       References:
#           http://michelanders.blogspot.ru/2010/12/calulating-sunrise-and-sunset-in-python.html
#           https://en.wikipedia.org/wiki/List_of_tz_database_time_zones
#
##########################################################################


################################
# Config
#

city_name = 'Denver'
audio_dir = '/pub/audio/nature/Sounds_of_Nature_Collection'

audiofile_dawn = '44_Predawn.mp3'
audiofile_morning = ''
audiofile_late_morning = ''

audiofile_noon = ''
audiofile_early_afternoon = ''
audiofile_afternoon = ''
audiofile_late_afternoon = ''

audiofile_early_dusk = ''
audiofile_dusk = ''
audiofile_night = ''


audiofile_00h = ''
audiofile_01h = ''
audiofile_02h = ''
audiofile_03h = ''
audiofile_04h = ''
audiofile_05h = ''
audiofile_06h = ''
audiofile_07h = ''
audiofile_08h = ''
audiofile_09h = ''
audiofile_11h = ''
audiofile_12h = ''
audiofile_13h = ''
audiofile_14h = ''
audiofile_15h = ''
audiofile_16h = ''
audiofile_17h = ''
audiofile_18h = ''
audiofile_19h = ''
audiofile_20h = ''
audiofile_21h = ''
audiofile_22h = ''
audiofile_23h = ''



###############################
# Code
#
import time
import os
import mad # pymad
import pygame
import datetime
from astral import Astral


def get_mp3_length( mp3_file ):
    # This returns the length in mili-seconds of the mp3 file
    audio = mad.MadFile(mp3_file)
    mp3_length = audio.total_time() 
    print "mp3 length: %d" % mp3_length
    return mp3_length

audio_file = audio_dir + "/" + audiofile_dawn

print audio_file
lengthy = get_mp3_length(audio_file)
print lengthy
