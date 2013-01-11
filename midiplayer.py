#!/usr/bin/python
import globals as c
import pygame

def initializeMidiPlayer(guiSelf, midiFilename):
	# initialize settings
	freq = 44100
	bitsize = -16
	channels = 2
	buffer = 102
	pygame.mixer.init(freq, bitsize, channels, buffer)
	
	# load midi file
	pygame.mixer.music.load(midiFilename)
	return True

def stopOrPlay(guiSelf):
	if pygame.mixer.music.get_busy():
		stopAll(guiSelf)
	else:
		playAll()
	return c.IS_PLAYING

def stopAll(guiSelf):
	if c.IS_PLAYING and pygame.mixer.music.get_busy():
		pygame.mixer.music.stop()
		#print "Midi " + str(c.MIDI_FILENAME_SHORT) + " stopped."
	guiSelf.resetImages()
	c.CURRENT_EVENT = 0
	c.IS_PLAYING = False
	return

def playAll():
	pygame.mixer.music.play(0)
	#print "\nMidi " + str(c.MIDI_FILENAME_SHORT) + " is playing..."
	c.CURRENT_EVENT = 0
	c.IS_PLAYING = True
	return
