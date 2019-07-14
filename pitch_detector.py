"""
Frequencies obtained from pages.mtu.edu/~suits/notefreqs.html
"""

import matplotlib.pyplot as plt
import numpy as np
import pyaudio
import time

# decide whether to display the FFT graph of the sound input
DISPLAY_GRAPH = False

# values for pyaudio microphone input
CHUNK = 4096
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

# band pass filter
MIN_FREQ = 50
MAX_FREQ = 2000
MIN_INDEX = MIN_FREQ*CHUNK/RATE
MAX_INDEX = MAX_FREQ*CHUNK/RATE

# significant peak value 
SIG_VAL = 30

# strictness of note definition
NOTE_WIDTH = 300

# exact frequency values for each musical note
FREQS = [ 
		  ('D2',73.42), ('D#2',77.78), ('E2',82.41),
		  ('F2',87.31), ('F#2',92.50), ('G2',98.00),
		  ('G#2',103.83), ('A2',110.00), ('A#2',116.54),
		  ('B2',123.54), ('C3',130.81), ('C#3',138.59),
		  ('D3',146.83), ('D#3',155.56), ('E3',164.81),
		  ('F3',174.61), ('F#3',185.00), ('G3',196.00),
		  ('G#3',207.65), ('A3',220.00), ('A#3',233.08),
		  ('B3',246.94), ('C4',261.63), ('C#4',277.18),
		  ('D4',293.66), ('D#4',311.13), ('E4',329.63),
		  ('F4',349.23), ('F#4',369.99), ('G4',392.00),
		  ('G#4',415.30), ('A4' ,440.00), ('A#4',466.16),
		  ('B4',493.88), ('C5',523.25), ('C#5',554.37),
		  ('D5',587.33), ('D#5',622.25), ('E5',659.26),
		  ('F5',698.46), ('F#5',739.99), ('G5',783.99),
		  ('G#5',830.61), ('A5',880,00), ('A#5',932.33),
		  ('B5',987.77), ('C6',1046.50), ('C#6',1108.73),
		  ('D6',1174.66), ('D#6',1244.51), ('E6',1318.51),
		  ('F6',1396.91), ('F#6',1479.98), ('G6',1567.98),
		  ('G#6',1661.22), ('A6',1760.00), ('A#6',1864.66),
		  ('B6',1975.53)
]

# acceptable ranges to define musical notes picked up by mic
FREQ_RANGES = [(tup[0],tup[1]/(2.0**(10.0/NOTE_WIDTH)),
			    tup[1],tup[1]*(2.0**(10.0/NOTE_WIDTH))) for tup in FREQS]

# extract maximum value from FFT
def filter(t, y):
	max_val = 0
	max_freq = 0
	for index in range(len(t)):
		if y[index] > max_val:
			max_freq = t[index]
			max_val = y[index]
	if max_val > SIG_VAL:
		return max_freq
	return 0

# translate frequency to musical note
def get_key(freq):
	for key in FREQ_RANGES:
		if float(freq) > key[1] and float(freq) < key[3]:
			return key[0]
	return 'NA'

# plot graph (y vs t) and update continuously
def continuous_plot(t, y, xlab, ylab):
	plt.plot(t, Y)
	plt.xlabel(xlab)
	plt.ylabel(ylab)
	plt.draw()
	plt.pause(0.0001)
	plt.clf()

# frequency domain
frq = np.arange(CHUNK)*RATE/CHUNK
frq = frq[MIN_INDEX:MAX_INDEX]

if __name__ == "__main__":

	# optional ask to display graph of FFT
	dg = raw_input("Display FFT graph? (y/n)\n")
	if dg == 'y':
		DISPLAY_GRAPH = True
		CHUNK = 8192

	p = pyaudio.PyAudio() # instantiate pyaudio object

	stream = p.open(format=FORMAT, # setup microphone
					channels=CHANNELS,
					rate=RATE,
					input=True,
					frames_per_buffer=CHUNK)

	while True:
		raw_data = np.fromstring(stream.read(CHUNK), dtype=np.int16) # record from mic
		data = np.fft.fft(raw_data) # perform FFT
		Y = abs(data[MIN_INDEX:MAX_INDEX])/CHUNK # band pass filter
		if DISPLAY_GRAPH:
			continuous_plot(frq, Y, "Frequency (Hz)", "Relative Magnitude")
		filt = filter(frq,Y)
		key = get_key(filt)
		print("DF: " + str(filt) + ", KEY: " + str(key)) # print freq and key

	stream.stop_stream()
	stream.close()
	p.terminate()
