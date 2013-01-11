#!/usr/bin/python
import globals as c
from midi import read_midifile
from re import search, split

def readMidiFile(guiSelf, midiFilename):
	try:
		# read midi file
		midiFilenameShort = midiFilename.split('/')[-1]
		midiFile = read_midifile(midiFilename)
	except TypeError as e:
		guiSelf.showError("ERROR: " + str(midiFilenameShort) + " is not a MIDI file.")
		return False
	
	# check midi format
	if midiFile.format == 0:
		guiSelf.showError("ERROR: " + str(midiFilenameShort) + " is in the wrong MIDI format. Please use a MIDI format 1 file.")
		return False
	
	# find drum tracks
	drumTrackList = getDrumTrackTitleList(midiFile)
	if drumTrackList == False:
		guiSelf.showError("ERROR: Could not find any drum tracks in " + str(midiFilenameShort) + ".")
		return False
	
	# get tempo
	multipleTempos = getTempo(midiFile)
	
	if multipleTempos:
		guiSelf.showError("WARNING: " + str(midiFilenameShort) + " contains multiple tempos, so plackback timing may be incorrect.")
	
	# update globals
	c.MIDI_FILE = midiFile
	c.DRUM_TRACK_TITLE_LIST = drumTrackList
	
	return True

def getDrumTrackTitleList(midiFile):
	numTracks = len(midiFile)
	trackIndexList = []
	titleList = []
	for trackIndex in range(0, numTracks):
		numEvents = len(midiFile[trackIndex])
		for eventIndex in range(0, numEvents):
			# determine the channel
			line = midiFile[trackIndex][eventIndex]
			find = search("midi.\w+\(tick=\d+, channel=(\d+)", str(line))
			
			# if the channel matches PERCUSSION_CHANNEL, it is a drum track
			if find != None:
				if int(find.group(1)) == c.PERCUSSION_CHANNEL:
					# add this track index to the track index list
					trackIndexList.append(trackIndex)
					
					# add this track title to the title list
					title = getTrackTitle(trackIndex, str(midiFile[trackIndex][0]))
					titleList.append(title)
					break
				else:
					break
	
	if len(trackIndexList) <= 0:
		# there are no drum tracks
		return False
	else:
		c.DRUM_TRACK_INDEX_LIST = trackIndexList
		return titleList

def getTrackTitle(trackIndex, titleLine):
	find = search("midi.TrackNameEvent\(tick=\d+, data=\[(.+)\]\)", str(titleLine))
	if find != None:
		# split up data
		characters = split(", ", (find.group(1)))
		
		# add each character to the title
		title = ""
		for character in characters:
			title = title + "" + chr(int(character))
		
		# add the track number to the title
		title = title + " (Track " + str(trackIndex) + ")"
	else:
		# titleLine is not a TrackNameEvent, so the title is just the track number
		title = "Track " + str(trackIndex)
	return title

def getTempo(midiFile):
	# default tempo
	tempTempo = ''
	
	# find a SetTempoEvent
	numEvents = len(midiFile[0])
	for eventIndex in range(0, numEvents):
		line = midiFile[0][eventIndex]
		find = search("midi.SetTempoEvent\(tick=\d+, data=\[(\d+), (\d+), (\d+)\]\)", str(line))
		if find != None:
			if tempTempo == '':
				tempTempo = int(line.get_bpm())
				c.TEMPO = tempTempo
			else:
				return True
	
	return False

def readDrumTrack(midiFile, drumTrackIndex):
	i = 0
	drumTrack = []
	numEvents = len(midiFile[drumTrackIndex])
	out = []
	accumlatedTicks = 0
	
	for eventIndex in range(0, numEvents):
		line = midiFile[drumTrackIndex][eventIndex]
		out.append(line)
		find = search("midi.Note(On|Off)Event\(tick=(\d+), channel=\d+, data=\[(\d+), (\d+)\]\)", str(line)) 
		if find != None:
			drumTrack.append([])
			if find.group(4) == "0":
				drumTrack[i].append("Off")
			else:
				drumTrack[i].append(str(find.group(1)))
			drumTrack[i].append(str(int(find.group(2)) + accumlatedTicks))
			drumTrack[i].append(str(find.group(3)))
			accumlatedTicks = 0
			i = i + 1
		else:
			findCCE = search("midi.ControlChangeEvent\(tick=(\d+), channel=\d+", str(line)) 
			if findCCE != None and findCCE.group(1) > 0:
				accumlatedTicks = accumlatedTicks + int(findCCE.group(1))
	
	#print "Drum track #" + str(drumTrackIndex) + " read successfully."
	return drumTrack
