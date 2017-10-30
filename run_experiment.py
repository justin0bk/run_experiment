import serial   
import threading
import PyCapture2
import numpy as np
import time
import subprocess
import matplotlib.pyplot as plt
import pyqtgraph as pg

# FUNCTION: Run and Stop Experiment
def main():
	global cam_on
	global start_time
	current_time = time.time()
	while current_time-start_time < delay*60 + exp_dur*60*60 and experiment_on:
		time.sleep(0.001)
		current_time = time.time()
	ComPort.write(bytearray(b'E\n'))
	cam_on = False

def terminate():
	global experiment_on
	global cam_on
	raw_input('Press enter to stop recording')
	experiment_on = False
	cam_on = False

# FUNCTION: Start Random Laser Stimulation
def run_laser():
	global start_time
	global delay #30*60 #30 minute delay before start
	global gap_min
	global gap_max
	time_total = delay*60 + exp_dur*60*60
	current_time = time.time()
	stim_gap = int(np.random.uniform(gap_min,gap_max)*60)
	ComPort2.write(bytearray(b'M' + str(delay*60 + stim_gap) + '\n'))

	# Counts for delay before stimulation cycles begin
	while current_time - start_time < delay*60 and experiment_on:
		time.sleep(0.001)
		current_time = time.time()
	
	# Start Stimulation Cycles
	t_stimStart = time.time()
	while time.time() - start_time < time_total - gap_max*60  and experiment_on:
		if time.time() - t_stimStart >= stim_gap:
			ComPort.write(bytearray(b'R\n'))
			laser_on = True
			time.sleep(laser_dur)
			laser_on = False
			stim_gap = int(np.random.uniform(gap_min,gap_max)*60)
			if time.time() - start_time < time_total - 25*60:
				ComPort2.write(bytearray(b'M' + str(stim_gap) + '\n'))
			t_stimStart = time.time()
		else:
			time.sleep(0.001)
		

# FUNCTION: Start Camera
def start_video():
	global start_time
	global image 
	vid_num = 1
	avi.MJPGOpen(title + str(vid_num), frame_rate, 20)
	c.startCapture()
	time.sleep(1) # Wait until camera powers on
	vid_start_time = time.time()
	c.writeRegister(pin2_strobecnt, StrobeOn)
	while cam_on is True:
		try:
			image = c.retrieveBuffer()
		except PyCapture2.Fc2error as fc2Err:
			print "Error retrieving buffer : ", fc2Err
			continue
		if time.time() - vid_start_time	> 3*60*60:  # If the video goes over 3 hours, it automatically opens up a new file
			avi.close()
			vid_num += 1
			vid_start_time = time.time()
			avi.MJPGOpen(title + str(vid_num), frame_rate, 20)
			avi.append(image)
			time.sleep(1.0/frame_rate)
		else:
			avi.append(image)
			# imgdat = image.getData()
			# imgnp = imgnp = np.array(imgdat).reshape(image.getRows(),image.getCols())
			# imv.setImage(imgnp)
			time.sleep(1.0/frame_rate)
	c.writeRegister(pin2_strobecnt, StrobeOff)
	avi.close()
	c.stopCapture()
	c.disconnect()

# def plt_playback():
# 	while cam_on:
# 		if bool(image):
# 			imgdat = image.getData()
# 			imgnp = imgnp = np.array(imgdat).reshape(image.getRows(),image.getCols())
# 			plt.imshow(imgnp)


####################################################################################
# Open rdh2000 interface (change directory to find the 'RHD2000interface.exe' file)
isrdhopen = raw_input('Is rdh2000 interface open? (y/n) ')
if isrdhopen == 'n':
	subprocess.Popen([r"C:\Users\WeberChungPC_03\Documents\Software\RHD2000\RHD2000interface.exe"])
	raw_input("Press Enter When You Complete the Acquisition Setting...\n")

mouse_num = input('How many mice are you recording from? ')
num_chans = []
mouse_IDs = []
title = ''
for i in range(mouse_num):
		num_chans.append(unicode.encode(raw_input('Specify channels for mouse #' + str(i+1) + ' (ex. MMEE) ')))
		mouse_name = unicode.encode(raw_input('Specify ID for mouse #' + str(i+1) + ' '))
		mouse_IDs.append(mouse_name)
		title += mouse_name

title += '_' + str(time.localtime().tm_mon)
title += str(time.localtime().tm_mday)
title += str(time.localtime().tm_year)[2:4] + '_'


# Initiate Arduino
ComPort = serial.Serial('COM5', rtscts = 0)
ComPort2 = serial.Serial('COM6', rtscts = 0)

# Initiate Camera Recording Setup
bus = PyCapture2.BusManager()
c = PyCapture2.Camera()
c.connect(bus.getCameraFromIndex(0))

# Setting Frame Rate
c.setProperty(type = PyCapture2.PROPERTY_TYPE.FRAME_RATE, autoManualMode = False)
c.setProperty(type = PyCapture2.PROPERTY_TYPE.FRAME_RATE, absControl = True)
c.setProperty(type = PyCapture2.PROPERTY_TYPE.FRAME_RATE, absValue = 5.0)
fRateProp = c.getProperty(PyCapture2.PROPERTY_TYPE.FRAME_RATE)
frame_rate = fRateProp.absValue

# Setting Video Mode
vidMOD = 0x604
MODE_0 = 0x00000000 #Full resolution
MODE_1 = 0x20000000 #Half resolution
MODE_5 = 0xA0000000 #Quarter resolution
c.writeRegister(vidMOD, MODE_1)

# Switching on Strobe Mode
GPIO_pin2_setting = 0x1130
GPIO_pin2_outVal = 0x80080001
pin2_strobecnt = 0x1508

StrobeOff = 0x80000000
StrobeOn = 0x82000000

c.writeRegister(GPIO_pin2_setting, GPIO_pin2_outVal)
c.writeRegister(pin2_strobecnt, StrobeOff)

# Add comments before start
comments = unicode.encode(raw_input('Any comments?'))

# Opening AVI file to save images
avi = PyCapture2.AVIRecorder()
# imv = pg.ImageView()
# imv.show()
raw_input('Press enter when you are ready to begin')

# Start Recording Data (Parameter setting)
experiment_on = True
cam_on = True
delay = 30 # Set delay in minutes
laser_on = False
laser_dur = 120 # Set the laser durations in seconds
exp_dur = 5 # Set the experiment duration in hours
gap_min = 5
gap_max = 15
sr = 1000

# image = 0
# plt.ion()

ComPort.write(bytearray('D' + str(laser_dur) + '\n'))
ComPort2.write(bytearray('T' + str(exp_dur*60*60 + delay*60 - 10) + '\n'))
time.sleep(1)

ComPort.write(bytearray(b'S\n'))
ComPort2.write(bytearray(b'S\n'))
start_time = time.time()

tv = threading.Thread(target = start_video, name = 'vid_thread')
tl = threading.Thread(target = run_laser, name = 'laser_thread')
tm = threading.Thread(target = main, name = 'main_thread)')
stop_exp = threading.Thread(target = terminate, name = 'check_stop_thread)')
# run_rt = threading.Thread(target = plt_playback, name = 'rt_playback')

stop_exp.start()
tm.start()
tv.start()
tl.start()
# run_rt.start()

stop_exp.join()
tm.join()
tv.join()
tl.join()
# run_rt.join()

ComPort.close()
ComPort2.close()

#Note parameters (currently overwrites preexisting parameter.txt file)
f = open(title + ".txt","w+")
f.write('SR:\t' + str(sr) + '\r\n')
f.write('delay:\t' + str(delay) + '\r\n')
f.write('laser_dur:\t' + str(laser_dur) + '\r\n')
f.write('exp_dur:\t' + str(exp_dur) + '\r\n')
f.write('mouse_ID:\t')
for i in range(len(mouse_IDs)):
	if i == len(mouse_IDs)-1:
		f.write(mouse_IDs[i])
	else:
		f.write(mouse_IDs[i] + '\t')
f.write('\r\n')
f.write('ch_alloc:\t')
for i in range(len(num_chans)):
	if i == len(num_chans)-1:
		f.write(str(num_chans[i]))
	else:
		f.write(str(num_chans[i]) + '\t')
f.write('\r\n')
f.write('note:\t' + comments + '\t')
f.close()

#####
# NOTE:
# variable that were changed: delay, stim_gap, laser_dur
#####
# Features to add:
# - mouse and channel selection (DONE)
# - time display (DONE)
# - title made automatically (DONE)
# - overwrite or add new parameters txt file (DONE)
# - add comments before experiment (DONE)
# - stop laser stimulation counting if less than 20 min remaining (DONE)
# - add real-time video using matplotlib
# - real-time spectrogram
#####
# - channel allocation
# - does changing channel order help?
# - laser dial number, type of laser

# Suggestions:
# could you put the variable initiation of gap_min and gap_max
# near exp_dur, as we might ofter want to change this parameter