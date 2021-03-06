APP_MAIN = ""

CANVAS_WIDTH = 635
CANVAS_HEIGHT = 306

DRUM_HI_HAT = 0
DRUM_LEFT_TOM = 1
DRUM_RIGHT_TOM = 2
DRUM_CRASH = 3
DRUM_SNARE = 4
DRUM_BASS = 5
DRUM_FLOOR_TOM = 6
DRUMS = [DRUM_HI_HAT, DRUM_LEFT_TOM, DRUM_RIGHT_TOM, DRUM_CRASH, DRUM_SNARE, DRUM_BASS, DRUM_FLOOR_TOM]

DRUM_NAME = []
KEY = []
NOTES = []
POS_TOP = []
POS_LEFT = []
for i in range (0, len(DRUMS)):
	DRUM_NAME.append("")
	KEY.append("")
	NOTES.append("")
	POS_TOP.append(0)
	POS_LEFT.append(0)

DRUM_NAME[DRUM_HI_HAT] = "hi-hat"
DRUM_NAME[DRUM_LEFT_TOM] = "high tom"
DRUM_NAME[DRUM_RIGHT_TOM] = "low tom"
DRUM_NAME[DRUM_CRASH] = "crash cymbal"
DRUM_NAME[DRUM_SNARE] = "snare drum"
DRUM_NAME[DRUM_BASS] = "bass drum"
DRUM_NAME[DRUM_FLOOR_TOM] = "floor tom"

CURRENT_EVENT = 0

DRUM_NUM = []
DRUM_TRACK = ""
DRUM_TRACK_TITLE_LIST = []
DRUM_TRACK_INDEX_LIST = []

INITIAL_WAIT = 0
IS_PLAYING = False

KEY[DRUM_HI_HAT] = 'j'
KEY[DRUM_LEFT_TOM] = 'd'
KEY[DRUM_RIGHT_TOM] = 'f'
KEY[DRUM_CRASH] = 'h'
KEY[DRUM_SNARE] = 's'
KEY[DRUM_BASS] = 'a'
KEY[DRUM_FLOOR_TOM] = 'g'

MAX_TEMPO = 300
MIN_TEMPO = 10

MIDI_FILE = ""
MIDI_FILENAME = ""
MIDI_FILENAME_SHORT = ""

NOTES[DRUM_HI_HAT] = [42, 44, 46]
NOTES[DRUM_LEFT_TOM] = [45, 47, 61, 64, 66, 68]
NOTES[DRUM_RIGHT_TOM ]= [48, 50, 60, 62, 63, 65, 67]
NOTES[DRUM_CRASH] = [49, 51, 52, 55, 57, 59]
NOTES[DRUM_SNARE] = [38, 40]
NOTES[DRUM_BASS] = [35, 36]
NOTES[DRUM_FLOOR_TOM] = [41, 43, 86, 87]

OUTPUT_MIDI_FILENAME = "output.mid"

PERCUSSION_CHANNEL = 9

POS_TOP[DRUM_HI_HAT] = 32
POS_TOP[DRUM_LEFT_TOM] = 15
POS_TOP[DRUM_RIGHT_TOM] = 15
POS_TOP[DRUM_CRASH] = 11
POS_TOP[DRUM_SNARE] = 130
POS_TOP[DRUM_BASS] = 97
POS_TOP[DRUM_FLOOR_TOM] = 122

POS_LEFT[DRUM_HI_HAT] = 11
POS_LEFT[DRUM_LEFT_TOM] = 197
POS_LEFT[DRUM_RIGHT_TOM] = 303
POS_LEFT[DRUM_CRASH] = 465
POS_LEFT[DRUM_SNARE] = 93
POS_LEFT[DRUM_BASS] = 198
POS_LEFT[DRUM_FLOOR_TOM] = 400

ROOT = ""

SETTINGS = {}

TEMPO = 120

WAIT_BEFORE = []
WAIT_AFTER = []