#!/usr/bin/python
import globals as c
from Tkinter import *
from guisettings import createSettingsInterface
from Image import open
from ImageDraw import Draw
from ImageTk import PhotoImage
from input import readMidiFile
from midiplayer import stopOrPlay, stopAll
from os import remove
from os.path import isfile
from playalong import initializePlayAlong, playAlong
from re import compile, IGNORECASE, search
from tkMessageBox import showinfo
from tkFileDialog import askopenfilename
import time

def createInterface():
	# create window
	c.ROOT = Tk()
	c.APP_MAIN = App(c.ROOT)
	c.ROOT.wm_title("MIDI Drum Trainer")
	c.ROOT.resizable(width=False, height=False)
	
	# enter interface loop
	c.ROOT.protocol("WM_DELETE_WINDOW", closeInterface)
	c.ROOT.mainloop()
	
	# end the program
	c.ROOT.destroy()
	
	return

def closeInterface():
	# stop currently playing song
	c.IS_PLAYING = False
	
	# close interface
	c.ROOT.quit()
	
	# destroy output file
	if isfile(c.OUTPUT_MIDI_FILENAME):
		remove(c.OUTPUT_MIDI_FILENAME)
	
	return

class App(Frame):
	def __init__(self, master):
		# initialize start up interface
		self.createButtons(master)
		self.createCanvas(master)
		self.initializeImages()
		
		# bind key presses to given functions
		c.ROOT.bind_all('<Key>', self.pressKey)
		c.ROOT.bind_all('<KeyRelease>', self.releaseKey)
		
		return
	
	def createButtons(self, frame):
		# create frame
		self.buttonFrame = Frame(frame)
		self.buttonFrame.grid(row=0, column=0, pady=10)
		
		# create load file button
		self.btnLoadFile = Button(self.buttonFrame)
		self.btnLoadFile["text"] = "Load File"
		self.btnLoadFile["command"] = self.loadFile
		self.btnLoadFile.grid(row=0, column=0, padx=5)
		
		# create play button
		self.btnPlay = Button(self.buttonFrame)
		self.btnPlay["command"] = self.playPause
		self.btnPlay["text"] = "Play"
		self.btnPlay["state"] = DISABLED
		self.btnPlay.grid(row=0, column=1, padx=5)
		
		return
	
	def createCanvas(self, frame):
		# create frame
		self.labelFrame = Frame(frame)
		self.labelFrame.configure(background="#ffffff")
		self.labelFrame.configure(borderwidth=0)
		self.labelFrame.grid(row=1, column=0)
		
		# create canvas
		self.canvas = Canvas(self.labelFrame)
		self.canvas.configure(background="#ffffff")
		self.canvas.configure(width=c.CANVAS_WIDTH)
		self.canvas.configure(height=c.CANVAS_HEIGHT)
		self.canvas.grid(row=0, column=0)
		
		return
	
	def initializeImages(self):
		# create arrays
		self.imgOff = []
		self.lblOff = []
		self.lblUser = []
		self.imgUser = []
		self.imgUser2 = []
		self.drawUser = []
		for i in range(0, len(c.DRUMS)):
			self.imgOff.append("")
			self.lblOff.append("")
			self.imgUser.append("")
			self.lblUser.append("")
			self.imgUser2.append("")
			self.drawUser.append("")
		
		# create the "on" image as a background
		self.imgBg = PhotoImage(file="images/drums_on.gif")
		self.lblBg = self.canvas.create_image(0, 0, anchor=NW, image=self.imgBg)
		
		# create the regular "off" images on top of the "on" images
		for i in c.DRUMS:
			self.imgOff[i] = PhotoImage(file="images/drum" + str(i) + "_off.gif")
			self.lblOff[i] = self.canvas.create_image(c.POS_LEFT[i], c.POS_TOP[i], anchor=NW, image=self.imgOff[i], tags="off" + str(i))
		
		# create the key labels overlay
		self.imgLabels1 = open(r"images/labels.png")
		self.drawLabels = Draw(self.imgLabels1)
		self.imgLabels= PhotoImage(self.imgLabels1)
		self.lblLabels = self.canvas.create_image(0, 0, anchor=NW, image=self.imgLabels)
		
		# create the "user on" images offscreen
		for i in c.DRUMS:
			self.imgUser[i] = open(r"images/drum" + str(i) + "_user.png")
			self.drawUser[i] = Draw(self.imgUser[i])
			self.imgUser2[i] = PhotoImage(self.imgUser[i])
			self.lblUser[i] = self.canvas.create_image(c.POS_LEFT[i], c.POS_TOP[i] + c.CANVAS_HEIGHT, anchor=NW, image=self.imgUser2[i], tags="user" + str(i))
		
		return
	
	def resetImages(self):
		for drumNum in c.DRUMS:
			# move all "off" images to initial onscreen position
			xOff, yOff = self.canvas.coords("off" + str(drumNum))
			self.canvas.move(self.lblOff[drumNum], -xOff + c.POS_LEFT[drumNum], -yOff + c.POS_TOP[drumNum])
			
			# move all "user on" images to initial offscreen position
			xUser, yUser = self.canvas.coords("user" + str(drumNum))
			self.canvas.move(self.lblUser[drumNum], 0, -yUser + c.CANVAS_HEIGHT + c.POS_TOP[drumNum])
		
		# update the interface
		c.ROOT.update()
		return
	
	def loadFile(self):
		# stop currently playing songs
		stopAll(self)
		
		# show dialog box
		self.options = {}
		self.options['filetypes'] = [('MIDI files', '.mid')]
		midiFilename = askopenfilename(parent=c.ROOT, title="Choose a MIDI file", **self.options)
		
		# ensure a file has been loaded
		if midiFilename != "":
			# ensure file is midi
			pattern = compile("\.midi?$", IGNORECASE)
			find = search(pattern, midiFilename) 
			if find != None:
				# read midi file
				success = readMidiFile(self, midiFilename)
				
				if success:
					c.MIDI_FILENAME = midiFilename
					c.MIDI_FILENAME_SHORT = c.MIDI_FILENAME.split('/')[-1]
					#print "\nMidi " + str(c.MIDI_FILENAME_SHORT) + " read successfully."
					
					# get settings
					createSettingsInterface()
			else:
				self.showError("ERROR: " + c.MIDI_FILENAME + " is not a MIDI file.")
				return False
		
		return
	
	def playPause(self):
		initSuccess = initializePlayAlong(self, c.DRUM_TRACK, int(c.TEMPO), c.MIDI_FILE.resolution)
		if initSuccess:
			isPlaying = stopOrPlay(self)
			if isPlaying == True:
				self.btnPlay["text"] = "Stop " + str(c.MIDI_FILENAME_SHORT)
				isComplete = playAlong(self, c.DRUM_TRACK)
				if isComplete:
					stopAll(self)
					self.btnPlay["text"] = "Restart " + str(c.MIDI_FILENAME_SHORT)
				else:
					self.btnPlay["text"] = "Play " + str(c.MIDI_FILENAME_SHORT)
			else:
				self.btnPlay["text"] = "Play " + str(c.MIDI_FILENAME_SHORT)
		return
	
	def noteOn(self, drumNum):
		# move regular drums offscreen
		a = time.clock()
		self.canvas.move(self.lblOff[drumNum], c.CANVAS_WIDTH, 0)
		c.ROOT.update()
		b = time.clock()
		return (b-a)
	
	def noteOff(self, drumNum):
		# move regular drums onscreen
		a = time.clock()
		self.canvas.move(self.lblOff[drumNum], -c.CANVAS_WIDTH, 0)
		c.ROOT.update()
		b = time.clock()
		return (b-a)
	
	def showError(self, message):
		showinfo("Error", message)
		return
	
	def pressKey(self, event):
		# find the drum that matches the key being pressed
		for drumNum in c.DRUMS:
			if event.char == c.KEY[drumNum] or event.char == c.KEY[drumNum].upper():
				# move highlighted drums onscreen
				xUser, yUser = self.canvas.coords("user" + str(drumNum))
				self.canvas.move(self.lblUser[drumNum], 0, -yUser + c.POS_TOP[drumNum])
				c.ROOT.update()
				
				# play the note (pygame.midi and pygame.music conflict, so this can't be used)
				#c.MIDI_OUT.note_on(c.NOTES[drumNum][0], 100, c.PERCUSSION_CHANNEL)
		return
	
	def releaseKey(self, event):
		# find the drum that matches the key being released
		for drumNum in c.DRUMS:
			if event.char == c.KEY[drumNum] or event.char == c.KEY[drumNum].upper():
				# move highlighted drums offscreen
				xUser, yUser = self.canvas.coords("user" + str(drumNum))
				self.canvas.move(self.lblUser[drumNum], 0, -yUser + c.CANVAS_HEIGHT + c.POS_TOP[drumNum])
				c.ROOT.update()
				
				# turn off the note (pygame.midi and pygame.music conflict, so this can't be used)
				#c.MIDI_OUT.note_off(c.NOTES[drumNum][0], 0, c.PERCUSSION_CHANNEL)
		return
