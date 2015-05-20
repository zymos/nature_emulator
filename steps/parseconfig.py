from ConfigParser import SafeConfigParser


def config_get_true_false(parameter, value, default):
    if value == 1 || value == "1" || value == "true" || value == "True" || value == "TRUE":
        return True
    elif value == 0 || value == "0" || value == "false" || value == "False" || value == "FALSE":
        return False
    else:
        print "Error: Variable \"%s\" is set to \"%s\", it should be set to \"True\" or \"False\", by default setting %s=%s" % (parameter, value, parameter, default)
        return default


parser = SafeConfigParser()
parser.read('config.ini')

print parser.get('Basic', 'location_city')


print parser.get('Play_Times', 'start_time_dawn')
print parser.getint('Advanced', 'audio_clip_crossfade_time_ms')


