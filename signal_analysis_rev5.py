import pandas as pd
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
import statistics as stat
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter, freqz

class PostProcess:
    def __init__(self, dataframe):
        self.df = dataframe
        self.rad_df = pd.DataFrame(columns=['Time', 'Voltage'])

    def graph(self):
        plt.plot(self.df['Time'], self.df['voltage'], label='Raw Signal')
        plt.title('Raw Signal')
        plt.xlabel('Time')
        plt.ylabel('Voltage')
        plt.legend()
        plt.show()

    def sd(self):
        sd = stat.stdev(self.df['voltage'])
        print(f'This is the standard deviation: {sd}')

    def welchpower(self):
        frequencies, psd = signal.welch(self.df['voltage'], 300, nperseg=1024)

        plt.figure(figsize=(10, 5))
        plt.semilogy(frequencies, psd)
        plt.title('Welch Power Spectral Density Estimate')
        plt.xlabel('Frequency (Hz)')
        plt.ylabel('Power/Frequency (dB/Hz)')
        plt.grid(True)
        plt.show()

# Get frequency response
    def butter_bandpass(self, lowcut, highcut, fs, order=4):
        nyquist = 0.5 * fs
        low = lowcut / nyquist
        high = highcut / nyquist
        b, a = butter(order, [low, high], btype='band')
        return b, a

# Filter signal
    def butter_bandpass_filter(self, data, lowcut, highcut, fs, order=4):
        b, a = self.butter_bandpass(lowcut, highcut, fs, order=order)
        y = lfilter(b, a, data)
        return y

    def rad_filter(self, low, high, n=4, f=500):
        lowcut = low
        highcut = high
        order = n
        fs = f

        b, a = self.butter_bandpass(lowcut, highcut, fs, order)

        w, h = freqz(b, a, worN=8000)
        plt.figure(figsize=(10, 5))
        plt.plot(0.5 * fs * w / np.pi, np.abs(h), 'b')
        plt.title('Butterworth Bandpass Filter Frequency Response')
        plt.xlabel('Frequency [Hz]')
        plt.ylabel('Gain')
        plt.show()

        self.filtered_signal = self.butter_bandpass_filter(self.df['voltage'], lowcut, highcut, fs, order)

        plt.figure(figsize=(10, 5))
        plt.plot(self.df['Time'], self.df['voltage'], 'b-', label='Original Signal')
        plt.plot(self.df['Time'], self.filtered_signal, 'r-', linewidth=2, label='Filtered Signal')
        plt.title('Original and Filtered Signals')
        plt.xlabel('Time [seconds]')
        plt.ylabel('Amplitude')
        plt.legend()
        plt.show()

        #self.df['Time']
        #my_dataframe = pd.DataFrame(self.filtered_signal, columns=['filtered voltage'])
        #csvdf = pd.DataFrame()
        #csvdf = csvdf.assign(time=self.df['Time'])
        #csvdf = csvdf.assign(filtered_voltage=my_dataframe['filtered voltage'])
        # csvdf.to_csv('filteredsignaldata.csv')

    def getcounts(self, voltage_thresh=-0.06):
        vdrop = []
        particles = 0
        drop_thresh = voltage_thresh
        in_drop = False  # Flag to track if we are currently in a drop region
        time_window = 0.1
        last_count_time = 0  # Last ided count! 

        for time, voltage in zip(self.df['Time'], self.filtered_signal):
            if time - last_count_time > time_window:
                if voltage < drop_thresh:
                    vdrop.append((time, voltage))
                    in_drop = True
                elif in_drop and voltage > drop_thresh:
                    if len(vdrop) > 1:
                        particles += 1
                        #print('Identified a count!')

                        self.rad_df = pd.concat(
                            [self.rad_df, pd.DataFrame({'Time': [vdrop[-1][0]], 'Voltage': [vdrop[-1][1]]})],
                            ignore_index=True)
                        last_count_time = vdrop[-1][0]
                    in_drop = False
                    vdrop = []

        plt.figure(figsize=(10, 5))
        plt.plot(self.df['Time'], self.df['voltage'], 'b-', label='Original Signal')
        plt.plot(self.df['Time'], self.filtered_signal, 'r-', linewidth=2, label='Filtered Signal')
        plt.plot(self.rad_df['Time'], self.rad_df['Voltage'], 'go', markersize=8, label='Radiation Counts')
        plt.title('Original, Filtered, Radiation Counts Identified')
        plt.xlabel('Time [seconds]')
        plt.ylabel('Amplitude')
        plt.legend()
        plt.show()

        print(f'The number of radiation particles: {particles}')
        print(f'Radiation counts/ minute: {particles/self.df["Time"].max()*60}')


    def noise_sd(self, voltage_thresh=-0.06):
        prev = 0
        self.sd_df = pd.DataFrame(columns=['Time', 'voltage'])

        for time in self.rad_df['Time']:
            if prev > 0:
                current = time 
                desired_interval = self.df.query(f'Time > {prev + 0.2} and Time < {current - 0.2}')
                #self.sd_df = pd.concat([self.sd_df, desired_interval[['Time', 'voltage']]], ignore_index=True)
                self.sd_df = self.sd_df.merge(desired_interval, how = 'outer')

            prev = time
        
        plt.figure(figsize=(10, 5))
        plt.plot(self.df['Time'], self.df['voltage'], 'b-', label='Original Signal')
        plt.plot(self.df['Time'], self.filtered_signal, 'r-', linewidth=2, label='Filtered Signal')
        plt.plot(self.rad_df['Time'], self.rad_df['Voltage'], 'go', markersize=8, label='Radiation Counts')
        plt.plot(self.sd_df['Time'], self.sd_df['voltage'], 'ko', markersize=4, label='Standard Deviation Calculation Data')
        plt.title('Original, Filtered, Radiation Counts Identified')
        plt.xlabel('Time [seconds]')
        plt.ylabel('Amplitude')
        plt.legend()
        plt.show()
        
        print(f"Noise standard deviation: {round(stat.stdev(self.sd_df['voltage']),2)}")

dataRate = 500
df = pd.read_csv('testwelchtestdata11.csv')
p = PostProcess(df)
p.graph()
p.welchpower()
p.rad_filter(100, 160, f= dataRate)
p.getcounts(-.06)
p.noise_sd(-.06)
