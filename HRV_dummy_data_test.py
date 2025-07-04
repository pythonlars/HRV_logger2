import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.signal import medfilt
from scipy import stats
from datetime import datetime

rr_data = np.loadtxt('HRV_dummy_data.txt')
start_time = datetime.now()
meshering_time = input("Please enter meshering time : ")
rmssd_list = []

def clean_data(rr_data):
  cleaned_data = []
  
  for i, rr in enumerate(rr_data):
    rr = float(rr)  # Data already in milliseconds
    if 300 < rr < 2000:  # Keep only valid RR intervals
      cleaned_data.append(rr)
      
  print(f"Valid data points: {len(cleaned_data)}")
  print(f"Total data points: {len(rr_data)}")
  return np.array(cleaned_data)

def calculate_metrics(cleaned_data, start_time=None):
    global rmssd_list, meshering_time
    # Convert meshering_time to integer
    meshering_time_int = int(meshering_time)
    
    # Check if we have valid data
    if len(cleaned_data) == 0:
        print("No valid data points found")
        return 0, [], [], []
    
    # Calculate mean RR interval and heart rate (preserve existing outputs)
    mean_rr = np.mean(cleaned_data)
    hr_bpm = 60000/mean_rr
    
    # Calculate successive differences of RR intervals
    rr_diff = np.diff(cleaned_data)
    
    # Create time points based on RR intervals (in milliseconds)
    time_points = np.cumsum(cleaned_data[:-1]) / 1000  # Convert ms to seconds
    
    # Define time intervals based on meshering_time (in minutes)
    interval_times = []  # To store the time points (in minutes)
    interval_rmssd = []  # To store RMSSD values for each interval
    
    # Calculate RMSSD for each interval
    intervals = {}
    
    # First determine which interval each data point belongs to
    for i, time_point in enumerate(time_points):
        # Calculate which interval this point belongs to (starting from 1)
        interval_number = int(time_point / (meshering_time_int * 60)) + 1
        
        # Store the diff in the appropriate interval
        if interval_number not in intervals:
            intervals[interval_number] = []
        
        # Add the RR difference to this interval
        intervals[interval_number].append(rr_diff[i])
    
    # Now calculate RMSSD for each interval
    for interval_number, diffs in sorted(intervals.items()):
        if len(diffs) > 1:  # Need at least two points for RMSSD
            rmssd = np.sqrt(np.mean(np.square(diffs)))
            
            # Store results
            time_point = interval_number * meshering_time_int
            interval_times.append(time_point)
            interval_rmssd.append(rmssd)
            rmssd_list.append(rmssd)
    
    # No need to process last interval - already handled in the loop above
    
    # Print the original outputs
    print(f"Heart Rate: {hr_bpm:.2f} bpm")
    
    # Print the new required outputs
    print("\nRMSSD Measurements by Time Interval:")
    print(f"Time points (minutes): {interval_times}")
    print(f"RMSSD values: {[round(float(val), 2) for val in interval_rmssd]}")
    
    return hr_bpm, rmssd_list, interval_times, interval_rmssd

def main():
  cleaned_data = clean_data(rr_data)
  hr_bpm, rmssd_list, interval_times, interval_rmssd = calculate_metrics(cleaned_data, start_time)

if __name__ == '__main__':
  main()
  