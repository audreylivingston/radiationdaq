from serialconnect_rev1 import SerialConnect
from signal_analysis_rev5 import PostProcess
import numpy as np
import time
from scipy import signal
import matplotlib.pyplot as plt

# Initialize serial communication variables
portName = 'COM11'
baudRate   = 115200
dataRate   = 500
recordTime = 10
numDataPoints = recordTime * dataRate

dataNames = ['Time', 'voltage']
dataTypes = [  '=L',      '=f']

rate_c     = 'r' # Data rate command
stop_c     = 's' # Data rate command

commandTimes = [recordTime] # Time to send command
commandData  = [0] # Value to send over
commandTypes = ['s'] # Type of command

# Save data
save_name = 'straight_long_quiet1'
fileName     = 'test'+save_name + '.csv'

s = SerialConnect(portName, fileName, baudRate, dataRate, \
                  dataNames, dataTypes, commandTimes, commandData, commandTypes)

# Connect to Arduino and send over rate
s.connectToArduino()

# Collect data
while len(s.dataStore[0]) < numDataPoints:
    s.getSerialData()
    s.sendCommand()

    # print seconds passed
    if len(s.dataStore[0]) % dataRate == 0:
        print(len(s.dataStore[0]) /dataRate)   

# Close Arduino connection and save data
df = s.closeandgetdf()

# Start post-processing
dataRate = 500
p = PostProcess(df)
p.graph()
p.welchpower()
p.rad_filter(90, 160, f = dataRate)
p.getcounts(-.07)
p.noise_sd(-.07)