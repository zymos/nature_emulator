#!/usr/bin/env python
# from pygame import mixer
import time
import threading
import sys
import os.path
import re

DEBUG = True




####################################################################
# DEFAULT CONFIG
#
# there will be no error checking on these values,
# they are assume to be entered correctly
def get_default_config():
    global DEBUG

    config_default = {}

    config_default['GLOBAL_CONFIG_FILE'] = 'configure.ini'
    # config_default['LOCAL_CONFIG_FILE'] = 'config_local.ini'

    config_default['PRIMARY_AUDIO_DIRECTORY'] = 'audio'
    config_default['SECONDARY_AUDIO_DIRECTORY'] = ''

    config_default['CITY_LOCATION'] = 'Denver'

    config_default['ENABLE_WIFI'] = False
    config_default['WIFI_ACCESS_POINT'] = ''
    config_default['WIFI_PASSWORD'] = ''

    config_default['BACKGROUND_SOUND_ENABLE'] = True
    config_default['BACKGROUND_SOUND_FILENAME'] = '13_Streamside_Songbirds.ogg'
    config_default['BACKGROUND_SOUND_VOLUME'] = 70

    config_default['ENABLE_FIXED_TIME_MODE'] = True
    config_default['START_OF_THE_DAY_MODE'] = 'fixed'
    config_default['END_OF_THE_DAY_MODE'] = 'fixed'
    config_default['ENABLE_FIXED_LATENIGHT'] = True

    config_default['FIXED_TIME_DAWN'] = '05:00'
    config_default['FIXED_TIME_SUNRISE'] = '05:45'
    config_default['FIXED_TIME_MIDMORNING'] = '10:00'
    config_default['FIXED_TIME_MIDAFTERNOON'] = '15:00'
    config_default['FIXED_TIME_SUNSET'] = '20:15'
    config_default['FIXED_TIME_DUSK'] = '20:45'
    config_default['FIXED_TIME_LATENIGHT'] = '22:00'

    config_default['DAWN_AUDIO_FILENAME'] = '13_Streamside_Songbirds.ogg'
    config_default['SUNRISE_AUDIO_FILENAME'] = '13_Streamside_Songbirds.ogg'
    config_default['MIDMORNING_AUDIO_FILENAME'] = '13_Streamside_Songbirds.ogg'
    config_default['MIDAFTERNOON_AUDIO_FILENAME'] = '13_Streamside_Songbirds.ogg'
    config_default['SUNSET_AUDIO_FILENAME'] = '13_Streamside_Songbirds.ogg'
    config_default['DUSK_AUDIO_FILENAME'] = '13_Streamside_Songbirds.ogg'
    config_default['LATENIGHT_AUDIO_FILENAME'] = '13_Streamside_Songbirds.ogg'

    config_default['OVERLAP_TIME'] = 120
    config_default['AUDIO_FADE_TIME'] = 20
    config_default['DEBUG'] = True
    config_default['AUDIO_CROSSFADE_TIME'] = 2000

    DEBUG = config_default['DEBUG']

    return config_default


####################################################################
# A boolean checker with some Debug code
def truth_or_dare2(config_type, param_name, value):

    if  value == "1" or ( re.search('true|on|set|yes', value, re.IGNORECASE) is not None):
        if DEBUG:
            print "\t\t>> Config: %s file [%s] is true" % (config_type, param_name)
        return True
    elif  value == "0" or ( re.search('false|off|unset|no', value, re.IGNORECASE) is not None):
        if DEBUG:
            print "\t>> Config: %s file [%s] is false" % (config_type, param_name)
        return False
    else:
        # print "\t>>   and is not 0/1, off/on, false/true, unset/set" 
        if DEBUG:
            print "\t>> Error: %s file [%s] is not true or false" % (config_type, param_name)        
        return None
# truth_or_dare2 (end)




####################################################################
# A boolean checker with some Debug code
def truth_or_dare(param_name, param_global, param_user):

    #global
    if DEBUG:
         print "\t>> Config: GLOBAL file [%s]" % (param_name)    
    if  param_global == "1" or ( re.search('true|on|set|yes', param_global, re.IGNORECASE) is not None):
        global_true = 1
        if DEBUG:
            print "\t\t>> Config: GLOBAL file [%s] is true" % (param_name)
    elif  param_global == "0" or ( re.search('false|off|unset|no', param_global, re.IGNORECASE) is not None):
        global_true =  0
        if DEBUG:
            print "\t>> Config: GLOBAL file [%s] is false" % (param_name)
    else:
        # print "\t>>   and is not 0/1, off/on, false/true, unset/set" 
        global_true = 3
        if DEBUG:
            print "\t>> Config error: GLOBAL file [%s] is not true or false" % (param_name)        

    # user
    if DEBUG:
         print "\t>> Config: USER file [%s]" % (param_name)       
    if  param_user == "1" or ( re.search('true|on|set|yes', param_user, re.IGNORECASE) is not None):
        user_true = 1
        if DEBUG:
            print "\t\t>> Config: USER file [%s] is true" % (param_name)   
    elif  param_global == "0" or ( re.search('false|off|unset|no', param_global, re.IGNORECASE) is not None):
        user_true =  0
        if DEBUG:
             print "\t>> Config: USER file [%s] is false" % (param_name)                       
    else:
        # print "\t>>   and is not 0/1, off/on, false/true, unset/set" 
        user_true = 3
        if DEBUG:
            print "\t>> Config error: USER file [%s] is not true or false" % (param_name)                   

    if user_true == 3 and global_true == 3:
        print "%s: Fatal error: config variable, [%s] is not a directory" % (time.strftime("%H:%M:%S"), param)
        print "  >> %s" % (config[param])
        sys.exit(1)
    elif not global_true == 3:
        if global_true == 0:
            print "  >> Config: [%s] is False" % (param_name)     
            return False
        else:
            print "  >> Config: [%s] is True" % (param_name)            
            return True
    else:
        if user_true == 0:
             print "  >> Config: [%s] is False" % (param_name) 
             return False
        else:
            print "  >> Config: [%s] is True" % (param_name)            
            return True
# truth_or_dare (end)





# if param = 1, true, on, set, or yes
def is_true(param):
    if  param == "1" or ( re.search('true|on|set|yes', param, re.IGNORECASE) is not None):
        return True
    else:
        return False
# is_true (END)




# if param = 0, false, off, unset, or no
def is_false(param):
    if param == "0" or (re.search('false|off|unset|no', param, re.IGNORECASE) is not None):
        return True
    else:
        return False
# is_false (END)
#


    
# check if a string is a float:
def is_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False




# check time format, 24-hour clock, HH:MM
def is_time_format(value):
    if DEBUG:
        print "\t\t>> is_time_format(%s)" % value
    try:
        time.strptime(value, '%H:%M')
        return True
    except ValueError:
        return False





####################################################################
# Get the volume from the config string
def get_volume(param, value):
    if is_float(value):
        # is a valid float
        value = float(value)        
        if value > 100: # volume > 100
            if DEBUG:
                print "\t\t>> Config error: %s greater than 100%%, setting to 100%%" % (param)
            return 100.0
        elif value < 0: # volume is negative
            if DEBUG:
                print "\t\t>> Config error: %s is negative, setting to 0%%" % (param)
            return 0.0
        else: # volume is good
            # if DEBUG:
                # print "\t\t>> Config: %s is set to %s%%" % (param, value)
            return value
    else:
        # not a number
        if DEBUG:
            print "\t\t>> Config error: %s is not a number, ignoring" % (param)
        return None



def hm_to_seconds(t):
    h, m = [int(i) for i in t.split(':')]
    return 3600*h + 60*m



##################################################################
# This checks values of configs and corrects them
#
def correct_family_values(config_type, config_in):

    params = [  "LOCAL_CONFIG_FILE", 
    "PRIMARY_AUDIO_DIRECTORY",
    "SECONDARY_AUDIO_DIRECTORY",
    "CITY_LOCATION",
    "ENABLE_WIFI",
    "WIFI_ACCESS_POINT",
    "WIFI_PASSWORD",
    "BACKGROUND_SOUND_ENABLE",
    "BACKGROUND_SOUND_FILENAME",
    "BACKGROUND_SOUND_VOLUME",
    "ENABLE_FIXED_TIME_MODE",
    "START_OF_THE_DAY_MODE",
    "END_OF_THE_DAY_MODE",
    "ENABLE_DAWN_AUDIO",
    "ENABLE_MORNING_AUDIO",
    "ENABLE_MIDDAY_AUDIO",
    "ENABLE_DUSK_AUDIO",
    "ENABLE_NIGHT_AUDIO",
    "FIXED_TIME_DAWN",
    "FIXED_TIME_SUNRISE",
    "FIXED_TIME_MIDMORNING",
    "FIXED_TIME_MIDAFTERNOON",
    "FIXED_TIME_SUNSET",
    "FIXED_TIME_DUSK",
    "FIXED_TIME_LATENIGHT",
    "DAWN_AUDIO_FILENAME",
    "MORNING_AUDIO_FILENAME",
    "MIDDAY_AUDIO_FILENAME",
    "EVENING_AUDIO_FILENAME",
    "DUSK_AUDIO_FILENAME",
    "NIGHT_AUDIO_FILENAME",
    "DAWN_AUDIO_VOLUME",
    "MORNING_AUDIO_VOLUME",
    "MIDDAY_AUDIO_VOLUME",
    "EVENING_AUDIO_VOLUME",
    "DUSK_AUDIO_VOLUME",
    "NIGHT_AUDIO_VOLUME",
    "OVERLAP_TIME",
    "AUDIO_FADE_TIME",
    "DEBUG",
    "AUDIO_CROSSFADE_TIME",
    "start_time",
    "stop_time"]

    #####################################################
    # Process each parameter for configs
    # 
    
    config_out = {}
    for param in params:
        # global config
        # config_source[param] = 'none'
        # config[param] = ''
        if not config_in.has_key(param):
            config_out[param] = None
            if DEBUG:
                print "\t>> %s config [%s] is missing" % (config_type, param)
        elif config_in[param] == "" or config_in[param] == "''" or config_in[param] == "\"\"" :
            config_out[param] = None
            if DEBUG:
                    print "\t>> %s config [%s] is blank" % (config_type, param) 
        else:
            config_out[param] = config_in[param].translate(None, '\"\'')
            if DEBUG:
                print "\t>> %s config [%s]=[%s]" % (config_type, param, config_out[param])   
    # e
  

    if DEBUG:
        print "\t>> Scripts location: [%s]" % (get_script_path())




    ###############################################
    # LOCAL_CONFIG_FILE
    #
    param = 'LOCAL_CONFIG_FILE'
    
    if config_type == "LOCAL":
        config_out[param] = None
        #ignoring
    elif config_out[param] is None:
        if DEBUG:
           print "\t>> %s config: %s is missing" % (config_type, param)
    # checking relative path
    elif os.path.isfile(os.path.normpath(os.path.join(get_script_path(), config_out[param]))):
        config_out[param] = os.path.normpath(os.path.join(get_script_path(), config_out[param]))
        if DEBUG:
            print "\t>> %s config:  %s is a relative path" % (config_type, param)
            print "\t>>   %s" % (config_out[param])
    #checking absolute path
    elif os.path.isfile(os.path.normpath(config_out[param])):
        config_out[param] = os.path.normpath(config_out[param])
        if DEBUG:
            print "\t>> %s config:  %s is an absolute path" % (config_type, param)
            print "\t>>   %s" % (config_out[param])
    else:
        config_out[param] = None
        if DEBUG:
            print "\t>> %s config: %s does not exist" % (config_type, param)




    ###############################################
    # Audio directories
    #
    # Process AUDIO_DIR
    params = ['PRIMARY_AUDIO_DIRECTORY', 'SECONDARY_AUDIO_DIRECTORY']
    for param in params:
        # config[param] = config[param]
        # config[param] = config[param].translate(None, '\"\'')
        if DEBUG:
            print "\t>> config: [%s]" % (param)
        if config_out[param] is None:
            if DEBUG:
               print "\t>> %s config: %s is missing" % (config_type, param)
        # checking relative path
        elif os.path.isdir(os.path.normpath(os.path.join(get_script_path(), config_out[param]))):
            config_out[param] = os.path.normpath(os.path.join(get_script_path(), config_out[param]))
            if DEBUG:
                print "\t>> %s config:  %s is a relative path" % (config_type, param)
                print "\t>>   %s" % (config_out[param])
        #checking absolute path
        elif os.path.isdir(os.path.normpath(config_out[param])):
            config_out[param] = os.path.normpath(config_out[param])
            if DEBUG:
                print "\t>> %s config:  %s is an absolute path" % (config_type, param)
                print "\t>>   %s" % (config_out[param])




    ##############################################
    # Background sound
    #
    param = 'BACKGROUND_SOUND_ENABLE'
    config_out[param] = truth_or_dare2(config_type, param, config_out[param])
    # Background sound enable
    if config_out['BACKGROUND_SOUND_ENABLE']:
        # background sound filename
        param = 'BACKGROUND_SOUND_FILENAME'
        # Dont check file location yet
        # if not get_audiofile_location2(config_type, param, config_out[param], config_out['PRIMARY_AUDIO_DIRECTORY'], config_out['SECONDARY_AUDIO_DIRECTORY']) == None:
            # background sound filename is valid
            # config_out[param] = get_audiofile_location2(config_type, param, config_out[param], config_out['PRIMARY_AUDIO_DIRECTORY'], config_out['SECONDARY_AUDIO_DIRECTORY'])
            # print "\t>> %s config: BACKGROUND_SOUND is enabled" % (config_type)
            # print "\t>> %s Config: BACKGROUND_SOUND_FILENAME is " % (config_type)
            # print "\t %s" % (config_out['BACKGROUND_SOUND_FILENAME'])
        if is_audiofile(config_out[param]):
            # Setting BACKGROUND_SOUND_VOLUME
            if DEBUG:
                print "\t>> %s config, BACKGROUND_SOUND_FILENAME is [%s]" % (config_type, config_out[param])
            param = 'BACKGROUND_SOUND_VOLUME'
            if is_float(config_out[param]):
                # USER config's VOLUME is a float
                config_out[param] = get_volume(param, config_out[param])
                if DEBUG:
                    print "\t>> %s config, BACKGROUND_SOUND_VOUME is [%s%%]" % (config_type, config_out[param])
            else:
                # BACKGROUND_SOUND_VOLUME is missing or invalid
                if DEBUG:
                    print "\t>> %s config: error: BACKGROUND_SOUND_VOLUME is invalid, BACKGROUND_SOUND is disabled" % (config_type)
                config_out['BACKGROUND_SOUND_ENABLE'] = False
                config_out['BACKGROUND_SOUND_FILENAME'] = None
                config_out['BACKGROUND_SOUND_VOLUME'] = None
        else: # file not mp3/wav/ogg
            if DEBUG:
                print "\t>> %s config: error: BACKGROUND_SOUND_VOLUME is not wav/ogg/mp3, BACKGROUND_SOUND is disabled" % (config_type)
            config_out['BACKGROUND_SOUND_ENABLE'] = False
            config_out['BACKGROUND_SOUND_FILENAME'] = None
            config_out['BACKGROUND_SOUND_VOLUME'] = None
    else: # BACKGROUND_SOUND_ENABLE is False
        if DEBUG:
            print "\t>> %s config: error: BACKGROUND_SOUND_VOLUME is not wav/ogg/mp3, BACKGROUND_SOUND is disabled" % (config_type)
        config_out['BACKGROUND_SOUND_ENABLE'] = False
        config_out['BACKGROUND_SOUND_FILENAME'] = None
        config_out['BACKGROUND_SOUND_VOLUME'] = None



    #################################################################
    # TIMES_OF_DAY modes
    #

    # MODES: checking TIME_OF_DAY - MODEs
    param = 'ENABLE_FIXED_TIME_MODE'
    config_out[param] = truth_or_dare2(config_type, param, config_out[param])

    param = 'ENABLE_DAWN_AUDIO'
    config_out[param] = truth_or_dare2(config_type, param, config_out[param])

    param = 'ENABLE_MORNING_AUDIO'
    config_out[param] = truth_or_dare2(config_type, param, config_out[param])   

    param = 'ENABLE_MIDDAY_AUDIO'
    config_out[param] = truth_or_dare2(config_type, param, config_out[param])

    param = 'ENABLE_DUSK_AUDIO'
    config_out[param] = truth_or_dare2(config_type, param, config_out[param])

    param = 'ENABLE_NIGHT_AUDIO'
    config_out[param] = truth_or_dare2(config_type, param, config_out[param])    

    check_times = False
    check_time_error = False
    param = 'START_OF_THE_DAY_MODE'
    if config_out[param] is not None:
        if re.search('fixed', config_out[param], re.IGNORECASE) is not None:            
            config_out[param] = 'fixed'
            check_times = True
        elif re.search('dawn', config_out[param], re.IGNORECASE) is not None:            
            config_out[param] = 'dawn'
        elif re.search('sunrise', config_out[param], re.IGNORECASE) is not None:            
            config_out[param] = 'sunrise'
        else:
            config_out[param] = None

    param = 'END_OF_THE_DAY_MODE'
    if config_out[param] is not None:
        if re.search('fixed', config_out[param], re.IGNORECASE) is not None:            
            config_out[param] = 'fixed'
            check_times = True
        elif re.search('dawn', config_out[param], re.IGNORECASE) is not None:            
            config_out[param] = 'dusk'
        elif re.search('sunrise', config_out[param], re.IGNORECASE) is not None:            
            config_out[param] = 'sunset'
        elif re.search('latenight', config_out[param], re.IGNORECASE) is not None:            
            config_out[param] = 'latenight'

        else:
            config_out[param] = None


    # Checking FIXED modes with TIMES
    # check_times = False
    if config_out['ENABLE_FIXED_TIME_MODE'] is None:
        # ENABLE_FIXED_TIME_MODE is not true or false so diabling all 
        # time mode valiables
        if DEBUG:
            print "\t>> %s config, ENABLE_FIXED_TIME_MODE is invalid" % (config_type)
            print "\t>> %s config, disabling START_OF_THE_DAY_MODE, END_OF_THE_DAY_MODE, ENABLE_FIXED_LATENIGHT, FIXED_TIME_DAWN, FIXED_TIME_SUNRISE, FIXED_TIME_MIDMORNING, FIXED_TIME_MIDAFTERNOON, FIXED_TIME_SUNSET, FIXED_TIME_DUSK, FIXED_TIME_LATENIGHT" % (config_type)
        config_out['START_OF_THE_DAY_MODE'] = None
        config_out['END_OF_THE_DAY_MODE'] = None
        config_out['ENABLE_FIXED_LATENIGHT'] = None
        config_out['FIXED_TIME_DAWN'] = None
        config_out['FIXED_TIME_SUNRISE'] = None
        config_out['FIXED_TIME_MIDMORNING'] = None
        config_out['FIXED_TIME_MIDAFTERNOON'] = None
        config_out['FIXED_TIME_SUNSET'] = None
        config_out['FIXED_TIME_DUSK'] = None
        config_out['FIXED_TIME_LATENIGHT'] = None
        # disable = True
        check_times = False
    elif config_out['ENABLE_FIXED_TIME_MODE']:
        # ENABLE_FIXED_TIME_MODE is true, checking fixed times_of_day
        config_out['START_OF_THE_DAY_MODE'] = None
        config_out['END_OF_THE_DAY_MODE'] = None
        config_out['ENABLE_FIXED_LATENIGHT'] = None
        # disable = False
        check_times = True
        # Check is each of the FIXED_TIME_* are valid formats
    else: # FIXED_TIME_MODE is false
        if config_out['START_OF_THE_DAY_MODE'] == "fixed":
            # disable = False
            check_times = True
        if config_out['END_OF_THE_DAY_MODE'] == "fixed":
            # disable = False
            check_times = True
        # config_out['ENABLE_FIXED_TIME_MODE'] = False
        

    ##############################    
    # TIMES: checking FIXED_TIME_*
    # check_times_error = False
    if check_times: # checking times is needed
        check_times_error = False
        param = 'FIXED_TIME_DAWN'
        if not is_time_format(config_out[param]):
            check_times_error = True
            if DEBUG:
                print "\t>> %s config, %s time format is invalid" % (config_type, param)
        param = 'FIXED_TIME_SUNRISE'
        if not is_time_format(config_out[param]):
            check_times_error = True
            if DEBUG:
                print "\t>> %s config, %s time format is invalid" % (config_type, param)
        param = 'FIXED_TIME_MIDMORNING'
        if not is_time_format(config_out[param]):
            check_times_error = True
            if DEBUG:
                print "\t>> %s config, %s time format is invalid" % (config_type, param)
        param = 'FIXED_TIME_MIDAFTERNOON'
        if not is_time_format(config_out[param]):
            check_times_error = True
            if DEBUG:
                print "\t>> %s config, %s time format is invalid" % (config_type, param)
        param = 'FIXED_TIME_SUNSET'
        if not is_time_format(config_out[param]):
            check_times_error = True
            if DEBUG:
                print "\t>> %s config, %s time format is invalid" % (config_type, param)
        param = 'FIXED_TIME_DUSK'
        if not is_time_format(config_out[param]):
            check_times_error = True
            if DEBUG:
                print "\t>> %s config, %s time format is invalid" % (config_type, param)
        param = 'FIXED_TIME_LATENIGHT'
        if not is_time_format(config_out[param]):
            check_times_error = True
            if DEBUG:
                print "\t>> %s config, %s time format is invalid" % (config_type, param)
        # Check if FIXED_TIME_*, times_of_day, are in the correct order
        # and are not the same
        if not check_times_error:
            if hm_to_seconds(config_out['FIXED_TIME_DAWN']) > hm_to_seconds(config_out['FIXED_TIME_SUNRISE']) or hm_to_seconds(config_out['FIXED_TIME_SUNRISE']) > hm_to_seconds(config_out['FIXED_TIME_MIDMORNING']) or hm_to_seconds(config_out['FIXED_TIME_MIDMORNING']) > hm_to_seconds(config_out['FIXED_TIME_MIDAFTERNOON']) or hm_to_seconds(config_out['FIXED_TIME_MIDAFTERNOON']) > hm_to_seconds(config_out['FIXED_TIME_SUNSET']) or hm_to_seconds(config_out['FIXED_TIME_SUNSET']) > hm_to_seconds(config_out['FIXED_TIME_DUSK']) or hm_to_seconds(config_out['FIXED_TIME_DUSK']) > hm_to_seconds(config_out['FIXED_TIME_LATENIGHT']):
                check_times_error = True
                if DEBUG:
                    print "\t>> %s config: error times of day are out of order" % (config_type)

    if check_times_error: # there is a error in time, call dr who
        config_out['ENABLE_FIXED_TIME_MODE'] = None
        config_out['START_OF_THE_DAY_MODE'] = None
        config_out['END_OF_THE_DAY_MODE'] = None
        config_out['FIXED_TIME_DAWN'] = None
        config_out['FIXED_TIME_SUNRISE'] = None
        config_out['FIXED_TIME_MIDMORNING'] = None
        config_out['FIXED_TIME_MIDAFTERNOON'] = None
        config_out['FIXED_TIME_SUNSET'] = None
        config_out['FIXED_TIME_DUSK'] = None
        config_out['FIXED_TIME_LATENIGHT'] = None
        if DEBUG:
            print "\t>> %s config: error found, ignoring ENABLE_FIXED_TIME_MODE, START_OF_THE_DAY_MODE, END_OF_THE_DAY_MODE, FIXED_TIME_DAWN, FIXED_TIME_SUNRISE, FIXED_TIME_MIDMORNING, FIXED_TIME_MIDAFTERNOON, FIXED_TIME_SUNSET, FIXED_TIME_DUSK, and FIXED_TIME_LATENIGHT for %s config" % (config_type, config_type)

    else: # no time errors found, format ok, order ok
        if DEBUG:
            print "\t>> %s config: %s OK [%s]" % (config_type, 'FIXED_TIME_DAWN', config_out['FIXED_TIME_DAWN'])
            print "\t>> %s config: %s OK [%s]" % (config_type, 'FIXED_TIME_SUNRISE', config_out['FIXED_TIME_SUNRISE'])
            print "\t>> %s config: %s OK [%s]" % (config_type, 'FIXED_TIME_MIDMORNING', config_out['FIXED_TIME_MIDMORNING'])
            print "\t>> %s config: %s OK [%s]" % (config_type, 'FIXED_TIME_MIDAFTERNOON', config_out['FIXED_TIME_MIDAFTERNOON'])
            print "\t>> %s config: %s OK [%s]" % (config_type, 'FIXED_TIME_SUNSET', config_out['FIXED_TIME_SUNSET'])
            print "\t>> %s config: %s OK [%s]" % (config_type, 'FIXED_TIME_DUSK', config_out['FIXED_TIME_DUSK'])
            print "\t>> %s config: %s OK [%s]" % (config_type, 'FIXED_TIME_LATENIGHT', config_out['FIXED_TIME_LATENIGHT'])

    ########################
    # Checking [Filenames]

    if not is_audiofile(config_out['DAWN_AUDIO_FILENAME']):
        config_out['DAWN_AUDIO_FILENAME'] = None
        if DEBUG:
            print "\t>> %s config: error %s is not an mp3, ogg or wav" % (config_type, 'DAWN_AUDIO_FILENAME')
    if not is_audiofile(config_out['MORNING_AUDIO_FILENAME']):
        config_out['MORNING_AUDIO_FILENAME'] = None
        if DEBUG:
            print "\t>> %s config: error %s is not an mp3, ogg or wav" % (config_type, 'MORNING_AUDIO_FILENAME')
    if not is_audiofile(config_out['MIDDAY_AUDIO_FILENAME']):
        config_out['MIDDAY_AUDIO_FILENAME'] = None
        if DEBUG:
            print "\t>> %s config: error %s is not an mp3, ogg or wav" % (config_type, 'MIDDAY_AUDIO_FILENAME')
    if not is_audiofile(config_out['EVENING_AUDIO_FILENAME']):
        config_out['EVENING_AUDIO_FILENAME'] = None
        if DEBUG:
            print "\t>> %s config: error %s is not an mp3, ogg or wav" % (config_type, 'EVENING_AUDIO_FILENAME')
    if not is_audiofile(config_out['DUSK_AUDIO_FILENAME']):
        config_out['DUSK_AUDIO_FILENAME'] = None
        if DEBUG:
            print "\t>> %s config: error %s is not an mp3, ogg or wav" % (config_type, 'DUSK_AUDIO_FILENAME')
    if not is_audiofile(config_out['NIGHT_AUDIO_FILENAME']):
        config_out['NIGHT_AUDIO_FILENAME'] = None
        if DEBUG:
            print "\t>> %s config: error %s is not an mp3, ogg or wav" % (config_type, 'NIGHT_AUDIO_FILENAME')


    #############################
    # Check individual volumes
    param = 'DAWN_AUDIO_VOLUME' 
    config_out['param'] = get_volume(param, config_out[param]) 
    if DEBUG: 
        if config_out[param] is None: 
            print "\t>> %s config, error %s invalid" % (config_type, param) 
        else: 
            print "\t>> %s config, %s [%s%%]" % (config_type, param, config_out[param])
    param = 'MORNING_AUDIO_VOLUME' 
    config_out['param'] = get_volume(param, config_out[param]) 
    if DEBUG: 
        if config_out[param] is None: 
            print "\t>> %s config, error %s invalid" % (config_type, param) 
        else: 
            print "\t>> %s config, %s [%s%%]" % (config_type, param, config_out[param])
    param = 'MIDDAY_AUDIO_VOLUME' 
    config_out['param'] = get_volume(param, config_out[param]) 
    if DEBUG: 
        if config_out[param] is None: 
            print "\t>> %s config, error %s invalid" % (config_type, param) 
        else: 
            print "\t>> %s config, %s [%s%%]" % (config_type, param, config_out[param])
    param = 'EVENING_AUDIO_VOLUME' 
    config_out['param'] = get_volume(param, config_out[param]) 
    if DEBUG: 
        if config_out[param] is None: 
            print "\t>> %s config, error %s invalid" % (config_type, param) 
        else: 
            print "\t>> %s config, %s [%s%%]" % (config_type, param, config_out[param])
    param = 'DUSK_AUDIO_VOLUME' 
    config_out['param'] = get_volume(param, config_out[param]) 
    if DEBUG: 
        if config_out[param] is None: 
            print "\t>> %s config, error %s invalid" % (config_type, param) 
        else: 
            print "\t>> %s config, %s [%s%%]" % (config_type, param, config_out[param])
    param = 'NIGHT_AUDIO_VOLUME' 
    config_out['param'] = get_volume(param, config_out[param]) 
    if DEBUG: 
        if config_out[param] is None: 
            print "\t>> %s config, error %s invalid" % (config_type, param) 
        else: 
            print "\t>> %s config, %s [%s%%]" % (config_type, param, config_out[param])


    return config_out
# correct_family_values (END)







def is_audiofile(filename):
    if re.search('mp3|wav|ogg', os.path.splitext(filename)[1], re.IGNORECASE) is not None:
        return True
    else:
        return False
# def is_audiofile (END)





def check_audiofile_existance(file_name, primary_dir, secondary_dir):
    if DEBUG:
        print "\t:>>file_name %s" % (file_name)
        print "\t:>> primary_dir %s" % (primary_dir)   
        print "\t:>> secondary_dir %s" % (secondary_dir)
        print "\t:>> prime+filename %s" % (os.path.join(primary_dir, file_name))
        print "\t:>> secondary+filename %s" % (os.path.join(secondary_dir, file_name))
        # print "\t:>> %s" % ()
        # print "\t:>> %s" % ()
        # print "\t:>> %s" % ()
    if os.path.isabs(file_name) and os.path.isfile(file_name):
        return file_name
    elif os.path.isfile(os.path.join(primary_dir, file_name)):
        return os.path.join(primary_dir, file_name)
    elif os.path.isfile(os.path.join(secondary_dir, file_name)):
        return os.path.join(secondary_dir, file_name)
    else:
        return None
# def check_audiofile_existance (END)



#####################################################
# Checks an audiofile's existance, if its an mp3/ogg/wav, 
# and it returns its full path
def get_audiofile_location2(config_type, param, value, primary_audio_directory, secondary_audio_directory):


    if value is not None: # it's not blank
        if is_audiofile(value): # check if actually mp3/wav/ogg
            if DEBUG:
                print "\t\t>> %s config, [%s] is an mp3, wav or ogg" % (config_type, param)
            if check_audiofile_existance(value, primary_audio_directory, secondary_audio_directory) is not None: # check if file exists
                audiofile_location = check_audiofile_existance(value, primary_audio_directory, secondary_audio_directory)
                if DEBUG:
                    print "\t\t>> %s config, [%s] is: " % (config_type, param)
                    print "\t\t>>  : %s" % (audiofile_location)
                return audiofile_location # you are a winner
            else: # file DNE
                if DEBUG:
                    print "\t\t>> %s config, [%s] not found" % (config_type, param)
                return None
        else: # not an mp3/wav/ogg
            if DEBUG:
                print "\t\t>> %s config, [%s] is not a wav/mp3/ogg file" % (config_type, param)
            return None
    # Trying GLOBAL config, USER config failed
    else:
        if DEBUG:
             print "\t\t\t>> %s config, [%s] is blank or missing" % (config_type, param)

        return None
# get_audiofile_location2 (END)






# returns an full file link to an audiofile
def get_audiofile_location(param, config_user_missing, config_global_missing, config_user, config_global, primary_audio_directory, secondary_audio_directory):

    if DEBUG:
        print "\t\t>> Checking [%s] file location" % (param)
        print "\t\t>> config_user_missing %s" % (config_user_missing)
        print "\t\t>> config_global_missing %s" % (config_global_missing)
        print "\t\t>> config_user %s" % (config_user)
        print "\t\t>> config_global %s" % (config_global)
        print "\t\t>> primary_audio_directory %s" % (primary_audio_directory)
        print "\t\t>> secondary_audio_directory %s" % (secondary_audio_directory)

    if not config_user_missing: # it's not blank
        if DEBUG:
            print "\t\t>> Checking for USER config filename"
        if is_audiofile(config_user): # check if actually mp3/wav/ogg
            if DEBUG:
                print "\t\t\t>> file is an mp3, wav or ogg"
            if check_audiofile_existance(config_user, primary_audio_directory, secondary_audio_directory) is not None: # check if file exists
                audiofile_location = check_audiofile_existance(config_user, primary_audio_directory, secondary_audio_directory)
                if DEBUG:
                    print "\t\t\t>> Using audiofile from USER config: "
                    print "\t: %s" % (audiofile_location)
                return audiofile_location # you are a winner
            else: # file DNE
                if DEBUG:
                    print "\t\t\t>> file not found, trying GLOBAL config"
        else: # not an mp3/wav/ogg
            if DEBUG:
                print "\t\t\t>> is not a wav, mp3, or ogg file, trying GLOBAL config"
    # Trying GLOBAL config, USER config failed
    elif not config_global_missing: 
        if DEBUG:
            print "\t\t>> Checking for GLOBAL config filename"


    # all has failed
    if DEBUG:
        print "\t>> No valid audiofile found"
    return None

# get_audiofile_location (END)





#########################################
# returns scripts location
def get_script_path():
        return os.path.dirname(os.path.realpath(sys.argv[0]))
# def get_script_path (END)





##############################################################
# read config file, return in a dictionary
#
def parse_config_file(config_type, config_filename):
    from ConfigParser import ConfigParser
    
    config_dic = {}
    
    if not os.path.exists(config_filename):
        print "%s: Error: %s config file does not exist [%s]" % (time.strftime("%H:%M:%S"), config_type, config_filename)
        config_dic['CONFIG_EXISTS'] = False
    else:
        config_dic['CONFIG_EXISTS'] = True

    # get global config values
    parser_dic = ConfigParser()
    parser_dic.optionxform = str
    parser_dic.read(config_filename)
    
    if DEBUG:
        print "\t>> %s Config file: %s" % (config_type, config_filename)
        # print "\t  >> %s Sections %s" % (config_type, parser_dic.sections())
    for section_name in parser_dic.sections():
        if DEBUG:
            print '\t >> %s Section: %s' % (config_type, section_name)
            # print '\t  >> %s Options: %s' % (config_type, parser_dic.options(section_name))
        for name, value in parser_dic.items(section_name):
            if DEBUG:
                print '\t   >> %s Value: %s = %s' % (config_type, name, value)
            config_dic[name] = value

    return config_dic



#########################################
# main configure
def configure():

    
    ###################################
    # get DEFAULT config
    #
    config_default = {}
    config_default = get_default_config()


    ###################################
    # get GLOBAL config
    #
    config_global = {}
    # get filename
    config_global_filename = config_default['GLOBAL_CONFIG_FILE']
    # get config
    config_global = parse_config_file('GLOBAL', config_global_filename)
    


    ##################################
    # get USER config
    #
    config_local = {}
    # get config
    if config_global.has_key('LOCAL_CONFIG_FILE'):
        config_local_filename = config_global['LOCAL_CONFIG_FILE']
        config_local = parse_config_file('LOCAL', config_local_filename)
    else:
        config_local['CONFIG_EXISTS'] = False


    ##################################
    # Check Values
    #
    # defaults are not checked
    config_global = correct_family_values('GLOBAL', config_global)
    # config = get_family_values(config_global,config_user)

    # # config_user_filename = config_default['LOCAL_CONFIG_FILE']
    # if not os.path.exists(config_user_filename):
        # print "%s: Fatal error: user config file does not exist [%s]" % (time.strftime("%H:%M:%S"), config_user_filename)
        # sys.exit(1)


    # # get user config values
    # parser_user = ConfigParser()
    # parser_user.optionxform = str
    # parser_user.read(config_user_filename)
    
    # config_user = {}
    # if DEBUG:
        # print "\t>>Config file: %s" % (config_user_filename)
        # print "\t>>  Sections %s" % parser_user.sections()
    # for section_name in parser_user.sections():
        # if DEBUG:
            # print '\t>>  Section:', section_name
            # print '\t>>    Options:', parser_user.options(section_name)
        # for name, value in parser_user.items(section_name):
            # if DEBUG:
                # print '\t>>    Value: %s = %s' % (name, value)
            # config_user[name] = value




    # get user config values
    # config_user = {}
    # if not os.path.exists(config_user_filename):
        # print "%s: User config file does not exist [%s], using global settings" % (time.strftime("%H:%M:%S"), config_user_filename)
        # config_user["exists"] = False
    # else:
        # config_user["exists"] = True
        # print "%s: User config file located [%s]" % (time.strftime("%H:%M:%S"), config_user_filename)

        # parser_user = ConfigParser()
        # parser_user.read(config_user_filename)
        # if DEBUG:
            # print "\t>>Config file: %s" % (config_user_filename)
            # print "\t>>  Sections %s" % parser_user.sections()
        # for section_name in parser_user.sections():
            # if DEBUG:
                # print '\t>>  Section:', section_name
                # print '\t>>    Options:', parser_user.options(section_name)
            # for name, value in parser_user.items(section_name):
                # if DEBUG:
                    # print '\t>>    Value: %s = %s' % (name, value)
                # config_user[name] = value



    # print config.sections()

    # import re
    # i = "sest"
    # print truth_or_dare("i", i)
    


    # print config.get('topsecret.server.com','ForwardX11')
    # 'SectionOne' in config
    # print "Yippy"
    # print "Hello %s. You are %s years old." % (Name, Age)
    return
# def configure (END)






#############################################################
# Code
#

# Main Function
def main():
    # main function

    print "\n\n\n"
    
    # CONFIGURE
    print "%s: Configuring..." % (time.strftime("%H:%M:%S"))
    configure()
    print "done."
    
    # while True:
        # print "."
        # time.sleep(60)
    
    # EXIT
    time.sleep(1)
    print "%s: Exiting...\n\n"% (time.strftime("%H:%M:%S"))
    return
# def main (END)






if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, SystemExit):
        print
        print "%s: Exiting...\n\n"% (time.strftime("%H:%M:%S"))
        sys.exit(1)


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
