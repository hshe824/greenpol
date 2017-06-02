import serial
ser = serial.Serial('COM6', baudrate = 9600, timeout=1)

while 1:
	testData = ser.readline()
	print(testData)