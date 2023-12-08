# radiationdaq
This repository will allow a user to filter raw data gathered from a geiger counter. 

## Hardware Required
- Any microcontroller (arduino driver scripts provided)
- Geiger sensor
- High voltage module
- Battery

## Software Required
- Python
- Arduino

# Steps
## Install Firmware to Microcontroller
After the hardware is configured and the high voltage module output is read into an analog input port, load the me379m_Arduino_AnalogDAQ_to_Python.ino file onto the Arduino. Please note, this file must be modified for other microcontrollers. 
![image](https://github.com/audreylivingston/radiationdaq/assets/98493997/fb1ac233-89c5-4aef-a4e3-19080904f0c8)

## Aquire and Analyze Data
Three python scripts will allow you to aquire and filter data. 

1. **pyarduino_rev4.py** - main script
2. **serialconnect_rev1.py** - class that connects to arduino to acquire data.
3. **signal_analysis_rev5.py** - class that has methods to filter the data using plot welch power density, apply butterworth filter, calculate noise standard deviation, count radiation/ min

Please note that hardware does not need to be configured to run the signal_analysis_rev5.py script as you can use the testwelchtestdata11.csv as sample raw data acquired from the radiation sensor.
