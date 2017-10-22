# convert digital input numbers into pulse TTLs and strobe TTLs
# digital input data file comes in uint16 format
# before using this function, use np.fromfile function,
# specify the dtype = 'unit16'

def dig2state(dig_in):
	strobe_ttl = []
	laser_ttl = []
	for i in dig_in:
		if i == int(5):
			strobe_ttl.append(0)
			laser_ttl.append(0)
		elif i == int(1):
			strobe_ttl.append(1)
			laser_ttl.append(0)
		elif i == int(3):
			strobe_ttl.append(1)
			laser_ttl.append(1)
		elif i == int(7):
			strobe_ttl.append(0)
			laser_ttl.append(1)
		elif i == int(4):
			strobe_ttl.append(0)
			laser_ttl.append(0)
	return strobe_ttl, laser_ttl