#!/usr/bin/python
import globals as c
from midi import Pattern
from re import search

def createOutputMidiFile(settings):
	# duplicate original midi file
	outputMidiFile = c.MIDI_FILE
	
	# find set tempo event
	numEvents = len(outputMidiFile[0])
	i = 0
	for eventIndex in range(0, numEvents):
		line = outputMidiFile[0][eventIndex]
		find = search("midi.SetTempoEvent\(tick=(\d+)", str(line))
		if find != None:
			i = eventIndex
			break
	
	# set new tempo
	outputMidiFile[0][i].set_bpm(int(settings["tempo"]))
	
	# mute tracks
	if settings["muteDrums"]:
		return createMutedDrumsMidiFile(settings, outputMidiFile)
	elif settings["drumsOnly"]:
		return createIsolatedDrumsMidiFile(settings, outputMidiFile)
	else:
		return outputMidiFile

def createMutedDrumsMidiFile(settings, outputMidiFile):
	outputTracks = []
	numTracks = len(outputMidiFile)
	i = 0
	for trackIndex in range(numTracks):
		if settings["drumTrackIndex"] == trackIndex:
			j = 0
		else:
			outputTracks.append([])
			numEvents = len(outputMidiFile[trackIndex])
			for eventIndex in range(numEvents):
				line = outputMidiFile[trackIndex][eventIndex]
				outputTracks[i].append(line)
			i = i + 1
	outputMidiFile = Pattern(tracks=outputTracks)
	outputMidiFile.resolution = c.MIDI_FILE.resolution
	return outputMidiFile

def createIsolatedDrumsMidiFile(settings, outputMidiFile):
	outputTracks = []
	numTracks = len(outputMidiFile)
	i = 0
	for trackIndex in range(numTracks):
		if settings["drumTrackIndex"] == trackIndex or trackIndex == 0:
			outputTracks.append([])
			numEvents = len(outputMidiFile[trackIndex])
			for eventIndex in range(numEvents):
				line = outputMidiFile[trackIndex][eventIndex]
				outputTracks[i].append(line)
			i = i + 1
	outputMidiFile = Pattern(tracks=outputTracks)
	outputMidiFile.resolution = c.MIDI_FILE.resolution
	return outputMidiFile
