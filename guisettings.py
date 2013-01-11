#!/usr/bin/python
import globals as c
from Tkinter import *
from midiplayer import initializeMidiPlayer
from input import readDrumTrack
from midi import write_midifile
from output import createOutputMidiFile
from tkMessageBox import showinfo

def createSettingsInterface():
	global SETTINGS_ROOT
	SETTINGS_ROOT = Toplevel()
	appSettings = AppSettings(SETTINGS_ROOT)
	SETTINGS_ROOT.resizable(width=False, height=False)
	
	SETTINGS_ROOT.protocol("WM_DELETE_WINDOW", closeInterface)
	SETTINGS_ROOT.focus_set()
	SETTINGS_ROOT.grab_set()
	SETTINGS_ROOT.transient(c.ROOT)
	SETTINGS_ROOT.wait_window(SETTINGS_ROOT)
	
	return

def closeInterface():
	pass

def updateSettings(self):
	# update tempo
	c.TEMPO = c.SETTINGS["tempo"]
	
	# read selected drum track
	drumTrackIndex = c.SETTINGS["drumTrackIndex"]
	c.DRUM_TRACK = readDrumTrack(c.MIDI_FILE, drumTrackIndex)
	
	# create output file
	outputMidiFile = createOutputMidiFile(c.SETTINGS)
	write_midifile(c.OUTPUT_MIDI_FILENAME, outputMidiFile)
	
	# initialize midi player
	success = initializeMidiPlayer(self, c.OUTPUT_MIDI_FILENAME)
	
	# update interface
	c.APP_MAIN.btnPlay["state"] = ACTIVE
	c.APP_MAIN.btnPlay["text"] = "Play " + str(c.MIDI_FILENAME_SHORT)
	
	return success

class AppSettings(Toplevel):
	def __init__(self, master):
		# initialize interface
		self.createWidgets(master)
		return
	
	def createWidgets(self, frameSettings):
		# create frame
		self.widgetFrame = Frame(frameSettings)
		self.widgetFrame.grid(row=0, column=0, padx=10, pady=10)
		
		# create drum track label
		self.lblDrumTrack = Label(self.widgetFrame)
		self.lblDrumTrack["text"] = "Select drum track:"
		self.lblDrumTrack.grid(row=0, column=0)
		
		# create drum track list
		self.lstDrumTrack = Listbox(self.widgetFrame, exportselection=0)
		self.lstDrumTrack.grid(row=1, column=0)
		for item in c.DRUM_TRACK_TITLE_LIST:
			self.lstDrumTrack.insert(END, item)
		if self.lstDrumTrack.size() < 10:
			self.lstDrumTrack["height"] = self.lstDrumTrack.size() + 1
		else:
			self.lstDrumTrack["height"] = 10
		self.lstDrumTrack.select_set(0)
		
		# create tempo label
		self.lblTempo = Label(self.widgetFrame)
		self.lblTempo["text"] = "Enter tempo (BPM):"
		self.lblTempo.grid(row=2, column=0)
		
		# create tempo box
		self.txtTempo = Entry(self.widgetFrame)
		self.txtTempo.insert(0, str(c.TEMPO))
		self.txtTempo.grid(row=3, column=0)
		
		# create mute checkbutton
		self.muteOn = IntVar()
		self.chkMute = Checkbutton(self.widgetFrame)
		self.chkMute["text"] = "Mute drums"
		self.chkMute["var"] = self.muteOn
		self.chkMute.grid(row=4, column=0)
		
		# create drums only checkbutton
		self.drumsOnly = IntVar()
		self.chkDrumsOnly = Checkbutton(self.widgetFrame)
		self.chkDrumsOnly["text"] = "Drums only"
		self.chkDrumsOnly["var"] = self.drumsOnly
		self.chkDrumsOnly.grid(row=5, column=0)
		
		# create OK button
		self.btnOK = Button(self.widgetFrame)
		self.btnOK["text"] = "OK"
		self.btnOK["command"] = self.ok
		self.btnOK.grid(row=6, column=0, padx=5)
		
		return
	
	def ok(self):
		c.SETTINGS = {}
		
		drumTrackIndexList = map(int, self.lstDrumTrack.curselection())
		if len(drumTrackIndexList) == 0:
			drumTrackIndexList.append(0)
		drumTrackIndex = c.DRUM_TRACK_INDEX_LIST[drumTrackIndexList[0]]
		c.SETTINGS.setdefault("drumTrackIndex", drumTrackIndex)
		
		try:
			tempo = int(self.txtTempo.get())
			c.SETTINGS.setdefault("tempo", tempo)
			
			if tempo > c.MAX_TEMPO or tempo < c.MIN_TEMPO:
				self.showError("ERROR: Tempo must be between " + str(c.MIN_TEMPO) + " and " + str(c.MAX_TEMPO) + " BPM.")
			else:
				muteDrums = self.muteOn.get()
				c.SETTINGS.setdefault("muteDrums", muteDrums)
				
				drumsOnly = self.drumsOnly.get()
				c.SETTINGS.setdefault("drumsOnly", drumsOnly)
				
				if muteDrums and drumsOnly:
					self.showError("ERROR: Please select one check box only.")
				else:
					success = updateSettings(self)
					
					if success:
						SETTINGS_ROOT.destroy()
		except ValueError as e:
			self.showError("ERROR: Please enter an integer.")
		
		return
	
	def showError(self, message):
		showinfo("Error", message)
		return
