#!/usr/bin/python
import globals as c
from time import sleep

def initializePlayAlong(guiSelf, drumTrack, tempo, resolution):
	# calculate drum nums for each event
	numEvents = len(drumTrack)
	c.DRUM_NUM = []
	for eventIndex in range(0, numEvents):
		c.DRUM_NUM.append(getDrumNum(drumTrack[eventIndex][2]))
	
	# calculate wait times for each event
	ticksPerSec = (tempo / 60.0) * resolution
	waitTimes = calculateWaitTimes(drumTrack, ticksPerSec)
	if waitTimes != None:
		c.WAIT_BEFORE = waitTimes["waitBefore"]
		c.WAIT_AFTER = waitTimes["waitAfter"]
	else:
		guiSelf.showError("ERROR: Could not read wait times. Please try another MIDI file.")
		return False
	
	return True

def getDrumNum(midiNote):
	numDrums = len(c.NOTES)
	for drumNum in range (0, numDrums):
		noteList = c.NOTES[drumNum]
		for note in noteList:
			if int(midiNote) == int(note):
				return drumNum
	return

def calculateWaitTimes(drumTrack, ticksPerSec):
	# initialize all wait times to zero
	i = 0
	numEvents = len(drumTrack)
	waitTimes = {}
	waitBefore = []
	waitAfter = []
	splitWait = 0
	for eventIndex in range(0, numEvents):
		waitBefore.append(0.0)
		waitAfter.append(0.0)
	
	# find wait time between notes
	while i < numEvents:
		while drumTrack[i][0] == "On":
			tick = float(drumTrack[i][1])
			if tick > 0:
				waitBefore[i] = tick / ticksPerSec
			i = i + 1
		
		wait = False
		while drumTrack[i][0] == "Off":
			tick = float(drumTrack[i][1])
			if wait != True:
				extraSleep = False
			if tick > 0:
				waitBefore[i] = (tick / ticksPerSec)
				if waitBefore[i] > 0:
					splitWait = waitBefore[i] / 2
					waitBefore[i] = waitBefore[i] - splitWait
					extraSleep = True
				else:
					extraSleep = False
			if i < (numEvents - 1):
				if drumTrack[i + 1][0] != "Off":
					wait = False
					if extraSleep:
						waitAfter[i] = waitAfter[i] + splitWait
				else:
					wait = True
			i = i + 1
			if i == (numEvents):
				waitTimes.setdefault("waitBefore", waitBefore)
				waitTimes.setdefault("waitAfter", waitAfter)
				return waitTimes

def playAlong(guiSelf, drumTrack):
	numEvents = len(drumTrack)
	#print "Starting playalong..."
	waitBefore = c.WAIT_BEFORE
	waitAfter = c.WAIT_AFTER
	drumNum = c.DRUM_NUM
	negWait = 0
	
	while c.CURRENT_EVENT < numEvents and c.IS_PLAYING == True:
		# turn notes on
		accumulatedNegWait = 0
		while drumTrack[c.CURRENT_EVENT][0] == "On" and c.IS_PLAYING == True:
			if waitBefore[c.CURRENT_EVENT] > 0:
				if (waitBefore[c.CURRENT_EVENT] - accumulatedNegWait) > 0:
					sleep(waitBefore[c.CURRENT_EVENT] - accumulatedNegWait)
				accumulatedNegWait = 0
			
			if drumNum[c.CURRENT_EVENT] != None:
				negWait = guiSelf.noteOn(drumNum[c.CURRENT_EVENT])
				accumulatedNegWait = accumulatedNegWait + negWait
			
			c.CURRENT_EVENT = c.CURRENT_EVENT + 1
		
		# turn notes off and sleep
		accumulatedNegWait = 0
		while drumTrack[c.CURRENT_EVENT][0] == "Off" and c.IS_PLAYING == True:
			if waitBefore[c.CURRENT_EVENT] > 0:
				if (waitBefore[c.CURRENT_EVENT] - accumulatedNegWait) > 0:
					sleep(waitBefore[c.CURRENT_EVENT] - accumulatedNegWait)
				accumulatedNegWait = 0
			
			if drumNum[c.CURRENT_EVENT] != None:
				negWait = guiSelf.noteOff(drumNum[c.CURRENT_EVENT])
				accumulatedNegWait = accumulatedNegWait + negWait
			
			if waitAfter[c.CURRENT_EVENT] > 0:
				if (waitAfter[c.CURRENT_EVENT] - accumulatedNegWait) > 0:
					sleep(waitAfter[c.CURRENT_EVENT] - accumulatedNegWait)
				accumulatedNegWait = 0
			
			c.CURRENT_EVENT = c.CURRENT_EVENT + 1
			
			# check for end of song
			if c.CURRENT_EVENT == (numEvents):
				#print "Playalong complete."
				return True
	
	#print "Playalong stopped."
	return False
