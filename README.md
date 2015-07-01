# nature\_emulator


# Components
* Rasberry Pi
* Real time clock - saves time on power off
* Class-D amplifier
* 2 Speakers
* USB drive - stores config, audiofiles and nature emulator software
* LCD screen - for time display and basic config
* Scrolling buttons - for setting time and basic config
* Error LED - displays basic errors that arn't shown on screen


# How it works
The Rasberry Pi runs a basic Linux OS, with a few scripts for basic operation.  A USB drive stores a configuration file, audio files, and the nature\_emulator software.  Software on the USB drive can configure the nature\_emulator can be edited manually.  Audio files can be added to to the drive, and set in the config.  The nature\_emulator software runs off the drive.  Configuration file, audio files, and the nature\_emulator software can be modified added and upgraded by removing the drive.

# Detailed operation
1. Rasberry Pi boots
2. init scripts
	* check for errors, display on LED
	* Loads screen
	* Detect USB drive and run nature_emulator
3. nature\_emulator
	1. Read config
	2. Detect errors, override if posible or indicate error
	2. Check if init scripts need to be updated
	2. Selected mode
		* Single play mode
		* Fixed time mode
		* Dynamic sunset/sunrise mode
		* Combination Fixed/Dynamic mode
	3. Detect current time
	4. Queue files to play for the day
	5. Wait for midnight
	6. Return to step 4.
		

# USB drive file structure
	configure.ini
	setup_windows.exe
	setup_linux
	setup_osx
	audiofiles/
	nature_emulator/
	nature_emulator/nature_emulator.py
	nature_emulator/audiofiles/


# TODO
* finish nature\_emulator soft
* create setup software
* create init scripts
	* LCD display
	* error LED
	* detect USB
* Add RTC hardware
* Add LCD hardware
* Create 3D model of container
* Test, test, test


# Sounds of Nature sources

http://justme.land/5-sources-for-fascinating-sounds-of-nature/


The Sounds of Nature Collection by Gaia, https://archive.org/details/Sounds\_of\_Nature\_Collection - Creative Commons - Attribution 3.0

British library – Listen to the sounds of nature - http://www.bl.uk/listentonature/main.html - Copyrighted

## Animal sounds
http://macaulaylibrary.org/ - copyrighted (huge library, short clips)
US Fish and Wildlife Service - https://archive.org/details/animalsounds1 - Public Domain (short clips)

## Bird Calls
http://www.xeno-canto.org/ - various licenses
