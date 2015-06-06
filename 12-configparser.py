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



    
# check if a string is a float:
def is_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False




# check time format, 24-hour clock, HH:MM
def is_time_format(input):
    try:
        time.strptime(input, '%H:%M')
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
                print "\t>> Config error: %s greater than 100%%, setting to 100%%" % (param)
            return 100.0
        elif value < 0: # volume is negative
            if DEBUG:
                print "\t>> Config error: %s is negative, setting to 0%%" % (param)
            return 0.0
        else: # volume is good
            if DEBUG:
                print "\t>> Config: %s is set to %s%%" % (param, value)
            return value
    else:
        # not a number
        if DEBUG:
            print "\t>> Config error: %s is not a number, setting to 0%%" % (param)
        return 0.0




##################################################################
# check config paramators for validity, nessessitym and existance
#
def get_family_values(config_global, config_user):
    config = {}
    config_missing = {}
    config_user_missing = {}
    config_global_missing = {}

    
    params = [  "PRIMARY_AUDIO_DIRECTORY",
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
    "ENABLE_FIXED_LATENIGHT",
    "FIXED_TIME_DAWN",
    "FIXED_TIME_SUNRISE",
    "FIXED_TIME_MIDMORNING",
    "FIXED_TIME_MIDAFTERNOON",
    "FIXED_TIME_SUNSET",
    "FIXED_TIME_DUSK",
    "FIXED_TIME_LATENIGHT",
    "DAWN_AUDIO_FILENAME",
    "SUNRISE_AUDIO_FILENAME",
    "MIDMORNING_AUDIO_FILENAME",
    "MIDAFTERNOON_AUDIO_FILENAME",
    "SUNSET_AUDIO_FILENAME",
    "DUSK_AUDIO_FILENAME",
    "LATENIGHT_AUDIO_FILENAME",
    "OVERLAP_TIME",
    "AUDIO_FADE_TIME",
    "DEBUG",
    "AUDIO_CROSSFADE_TIME",
    "start_time",
    "stop_time"]

    #####################################################
    # Process each parameter for global and user configs
    # for param in params:
        # print "config_default['%s'] = '%s'" % (param, config_global[param])
    
    config_source = {}
    for param in params:
        # global config
        config_source[param] = 'none'
        config[param] = ''
        if not config_global.has_key(param):
            config_global_missing[param] = True
        elif config_global[param] == "":
            config_global_missing[param] = True
        else:
            config_global_missing[param] = False
            config_source[param] = 'GLOBAL'
            config_global[param] = config_global[param].replace('"', "")
            # print config[param]
        # user config
        if not config_user.has_key(param):
            config_user_missing[param] = True
        elif config_user[param] == "":
            config_user_missing[param] = True
        else:
            config_user_missing[param] = False
            config_source[param] = 'USER'
            config_user[param] = config_user[param].translate(None, '\"\'')
        if DEBUG:
             print "\t>>Config: available parameter [%s]" % (param)   
             if config_global_missing[param]:
                print "\t\t>> global config [%s] is missing or blank" % (param)
             else:
                print "\t\t>> global config [%s] is set to [%s]" % (param, config_global[param])
             if config_user_missing[param]:
                 print "\t\t>> user config [%s] is missing or blank" % (param)
                 if config_global_missing[param]:
                     print "\t\t>>Config: No config found for [%s]" % (param)
                 else:
                        print "\t\t>>Config: using Default config for [%s]" % (param)
             else:
                 print "\t\t>> user config [%s] is set to [%s]" % (param, config_user[param])
                 print "\t\t>>Config: using User config for [%s]" % (param)
          

    if DEBUG:
        print "\t>> Scripts location: [%s]" % (get_script_path())



    ###############################################
    # Audio directories
    #
    # Process AUDIO_DIR
    param = 'PRIMARY_AUDIO_DIRECTORY'
    if DEBUG:
        print "\t>> config: [%s]" % (param)
        print "\t\t>> config: config [%s]" % (config[param])
        print "\t\t>> config_user_missing: [%s]" % (config_user_missing[param])
        print "\t\t>> config_user: [%s]" % (config_user[param])
        print "\t\t>> config_global_missing: [%s]" % (config_global_missing[param])
        print "\t\t>> config_global: [%s]" % (config_global[param])      
        print " os.path.normpath(os.path.join(get_script_path(), config_user[param]))) %s" % (os.path.normpath(os.path.join(get_script_path(), config_user[param])))

    params = ['PRIMARY_AUDIO_DIRECTORY', 'SECONDARY_AUDIO_DIRECTORY']
    for param in params:
        # config[param] = config[param]
        # config[param] = config[param].translate(None, '\"\'')
        if DEBUG:
            print "\t>> config: [%s]" % (param)
            print "\t\t>> config: source [%s]" % (config_source[param])
            print "\t\t>> config: = %s" % (config[param])
        if config_user_missing[param] and config_global_missing[param]:
            if param == 'PRIMARY_AUDIO_DIRECTORY':
                #fatal
                print "%s: Fatal error: config variable, [%s] is required" % (time.strftime("%H:%M:%S"), param)
                sys.exit(1)
            else: #SECONDARY_AUDIO_DIR
                print "%s: Config: SECONDARY_AUDIO_DIRECTORY is missing, disabling" % (time.strftime("%H:%M:%S"))
                config[param] = None
        # checking USER config, relative path
        elif os.path.isdir(os.path.normpath(os.path.join(get_script_path(), config_user[param]))) and not config_user_missing[param]:
            config[param] = os.path.normpath(os.path.join(get_script_path(), config_user[param]))
            print "%s: Config: using %s config for [%s]" % (time.strftime("%H:%M:%S"), 'USER', param)
            print "\t>>   %s" % (config[param])
        #checking USER config, absolute path
        elif os.path.isdir(os.path.normpath(config_user[param])) and not config_user_missing[param]:
            config[param] = os.path.normpath(config_user[param])
            print "%s: Config: using %s config for [%s]" % (time.strftime("%H:%M:%S"), 'USER', param)
            print "\t>>   %s" % (config[param])
        # checking GLOBAL config, relative path
        elif os.path.isdir(os.path.normpath(os.path.join(get_script_path(), config_global[param])))and not config_global_missing[param]:
            config[param] = os.path.normpath(os.path.join(get_script_path(), config_global[param]))
            print "%s: Config: using %s config for [%s]" % (time.strftime("%H:%M:%S"),'GLOBAL', param)
            print "\t>>   %s" % (config[param])
        #checking GLOBAL config, absolute path
        elif os.path.isdir(os.path.normpath(config_global[param])) and not config_global_missing[param]:
            config[param] = os.path.normpath(config_global[param])
            print "%s: Config: using %s config for [%s]" % (time.strftime("%H:%M:%S"),'GLOBAL', param)
            print "\t>>   %s" % (config[param])
        else:
            if param == 'PRIMARY_AUDIO_DIRECTORY':
                #fatal
                print "%s: Fatal error: no valid dir found for [%s]" % (time.strftime("%H:%M:%S"), param)
                sys.exit(1)
            else: #SECONDARY_AUDIO_DIR
                print "%s: Config: no valid dir found for [SECONDARY_AUDIO_DIRECTORY], disabling" % (time.strftime("%H:%M:%S"))
                config[param] = None
       

        # elif (config_source[param] == "user") and os.path.isdir(os.path.join(get_script_path(), config_global[param])):
            # config[param] = os.path.join(get_script_path(), config_global[param])
            # print "  >> Config: using %s config for [%s]" % (config_source[param], param)    
            # print "    >> %s" % (config[param])
        # elif (config_source[param] == "user") and os.path.isdir(config_global[param]):
            # config[param] = config_global[param]
            # print "  >> Config: using %s config for [%s]" % (config_source[param], param)    
            # print "    >> %s" % (config[param])
        # elif os.path.isdir(config[param]):
                # config[param] = config[param]
                # print "  >> Config: using %s config for [%s]" % (config_source[param], param)
                # print "    >> %s" % (config[param])
        # else:
            # print "%s: Fatal error: config variable, [%s] is not a directory" % (time.strftime("%H:%M:%S"), param)
            # print "  >> %s" % (config[param])
            # sys.exit(1)



    #############################################
    # WIFI todo
    param = "ENABLE_WIFI"



    ##############################################
    # Background sound
    #
    param = 'BACKGROUND_SOUND_ENABLE'
    config[param] = truth_or_dare(param, config_global[param], config_user[param])

    # Background sound enable
    if config['BACKGROUND_SOUND_ENABLE']:
        # background sound filename
        param = 'BACKGROUND_SOUND_FILENAME' 
        if DEBUG:
            print "\t>> Background sound enabling"
        if not get_audiofile_location(param, config_user_missing[param], config_global_missing[param], config_user[param], config_global[param], config['PRIMARY_AUDIO_DIRECTORY'], config['SECONDARY_AUDIO_DIRECTORY']) == None:
            # background sound filename is valid
            config[param] = get_audiofile_location(param, config_user_missing[param], config_global_missing[param], config_user[param], config_global[param], config['PRIMARY_AUDIO_DIRECTORY'], config['SECONDARY_AUDIO_DIRECTORY'])
            print "%s: Config: BACKGROUND_SOUND is enabled" % (time.strftime("%H:%M:%S"))
            print "%s: Config: BACKGROUND_SOUND_FILENAME is " % (time.strftime("%H:%M:%S"))
            print "\t %s" % (config['BACKGROUND_SOUND_FILENAME'])

            # Setting BACKGROUND_SOUND_VOLUME
            param = 'BACKGROUND_SOUND_VOLUME'
            if is_float(config_user[param]) and not config_user_missing[param]:
                # USER config's VOLUME is a float
                config[param] = get_volume(param, config_user[param])
                print "%s: Config: BACKGROUND_SOUND_VOUME is [%s%%] from USER config" % (time.strftime("%H:%M:%S"), config[param])
            elif is_float(config_global[param]) and not config_global_missing[param]:
                # GLOBAL config's VOLUME is a float
                config[param] = get_volume(param, config_global[param])
                print "%s: Config: BACKGROUND_SOUND_VOLUME is [%s%%] from GLOBAL config" % (time.strftime("%H:%M:%S"), config[param])
            else:
                # BACKGROUND_SOUND_VOLUME is missing or invalid
                print "%s: Config error: BACKGROUND_SOUND_VOLUME is invalid, BACKGROUND_SOUND is disabled" % (time.strftime("%H:%M:%S"))
                config['BACKGROUND_SOUND_ENABLE'] = False
        else: 
            #file not found, disabling
            print "%s: Config error: BACKGROUND_SOUND_FILENAME is invalid, BACKGROUND_SOUND is disabled" % (time.strftime("%H:%M:%S"))
            config['BACKGROUND_SOUND_ENABLE'] = False
    else: 
        # background sound disabled
        print "%s: Config: BACKGROUND_SOUND is disabled" % (time.strftime("%H:%M:%S"))

    
    ############################################
    # Times of day mode
    #
    param = 'ENABLE_FIXED_TIME_MODE'
    config[param] = truth_or_dare(param, config_global[param], config_user[param])

    if config[param]:
        param = 'FIXED_TIME_DAWN'
        param = 'FIXED_TIME_SUNRISE'
        param = 'FIXED_TIME_MIDMORNING'
        param = 'FIXED_TIME_MIDAFTERNOON'
        param = 'FIXED_TIME_SUNSET'
        param = 'FIXED_TIME_DUSK'
        param = 'FIXED_TIME_LATENIGHT'


    return config
# def get_family_values (END)





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
    config_global = check_family_values('GLOBAL', config_global)
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
