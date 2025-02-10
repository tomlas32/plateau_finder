"""
@author Tomasz Lasota
@version 1.0

This script processes temperature data from a temperature.txt file, analyzes temperature plateaus,
and summarizes channel statistics. It generates an Excel summary file containing
temperature data, statistics, and optionally plots the temperature profiles for each 
TSC file.

The main functionalities of the script include:
1. Reading and processing temperature.txt files.
2. Synchronizing temperature data based on specified thresholds.
3. Finding all available temperature holds (exact target temps are not required).
4. Exporting results to an Excel file with each file's data in separate sheets.
5. Plotting temperature data based on user-defined settings.

Returns:
- An Excel file named 'summaryYYYY-MM-DD.xlsx' containing the summarized data.
- Optional plots of temperature profiles for each processed data file.

Note: 
- The user can adjust the `plot_data` variable to `True` or `False` to enable or 
  disable the plotting of temperature data as needed.
- The user can adjust the 'find_plateaus' variable to `True` or `False` to enable or disable automated 
  plateaus findong. When disabled the hard-coded indexes will be used to summerise and plot the data.
- The user can also adjust the 'tolerance' parameter used to determine stability of a given segement (plataeu). 
  A higher tolerance value makes the 'find_distinct_plateaus' function less stringent, increasing the likelyhood
  of identifying plateaus in transitional regions where the data shifts between distinct plateaus.
  However, adjusting the 'tolerance' can help with identifying plateaus in lest stable regions of the data. 
- When using the `find_plateaus', ensure that the correct data slices are selected.
   - You can verify this by setting 'plot_data' to True and reviewing the highlighted regions (marked with thicker lines)
     to confirm they align with the expected plateaus.
  If the function does not identify the correct plateaus, you may need to use hardcoded indices. Note that these indices 
  may require adjustment based on the specific data set being analyzed.

"""

import os
import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from temp_analysis_utils import sum_channel_stats, find_distinct_plateaus



#USER TO SPECIFY PLOTTING REQ. 
plot_data = True
find_plateaus = True
num_points   = 1350 # ~30seconds
tolerance = 0.4


if __name__ == "__main__":

    # initilize variables
    columns = ["ch1", "ch2", "ch3", "ch4", "time"]
    ch_cols = ["red", "green", "blue", "black"]  # colors for each data channel
    df_dict = {}

    temp_start = 40 # threshold temperature for synchronization start time
    temp_sync_start = 35 # threshold start temperature for interpolation start time
    temp_sync_end = 45 # threshold end temperature for interpolation start time

    # get current date and time
    now = datetime.datetime.now().date()
    file_path = f"summary{now}.xlsx"

    # get list of txt files to be processed
    current_directory = os.getcwd()
    data_files = [file for file in os.listdir(current_directory) if file.endswith(".txt")]

    # Read, process and display data per .txt file
    for data_file in data_files:
        if data_file:

            # initialize list to store plateau start and end indices
            start_indicies = []
            end_indicies = []

            # hardcoded plateau indecies 
            start_index = [3650, 7150, 10550, 13750, 17250]
            end_index = [4999, 8499, 11899, 15099, 18599]
            
            # stores time at 40 degrees C used for plot synchronisation
            time_start = [] 

            try:
                # Read in .txt into pandas DataFrame
                with open(data_file, "r", encoding="utf-8", errors="ignore") as file:
                    df_data=pd.read_csv(file, skiprows=5, skipfooter=1, header=None, engine='python', 
                                            names=columns, on_bad_lines="skip")
                    
                #Find the correct data channel    
                channels = df_data.columns[(df_data.iloc[0] > 10) & (df_data.iloc[0] < 120)].tolist()
                
                # synchronise timing using sensor 1 temperature reaching time_start
                # find index range for synchronisation
                index_sync_start = next(x for x, val in enumerate(df_data[channels[0]]) if val > temp_sync_start)
                index_sync_end = next(x for x, val in enumerate(df_data[channels[0]]) if val > temp_sync_end)
                
                # synchronise timing using sensor 1 temperature reaching time_start
                times = df_data["time"][index_sync_start:index_sync_end]
                temps = df_data[channels[0]][index_sync_start:index_sync_end]

                time_start.append(np.interp(temp_start,temps,times))
                df_data["time"] = (df_data["time"]-time_start)/1000 

                df_data = df_data.iloc[index_sync_start:].reset_index()

                if find_plateaus:
                    # find temperature plateaus
                    plateau_list = find_distinct_plateaus(df = df_data, tolerance = tolerance, num_points=num_points, channels = channels, 
                                                    step_size = 100, plateau_threshold=1.0)
                    # get first and last index of each temp plateau
                    for i in range(len(plateau_list)):
                        start_indicies.append(plateau_list[i].index[0])
                        end_indicies.append(plateau_list[i].index[-1])
                        # calculate min, max and mean of each temperature plateau and pass it into a dictionary
                        df_dict[f"Plataeu_{i+1}"] = sum_channel_stats(plateau_list[i], channels, f"Plataeu_{i+1}")
                else:
                    # use hardcoded indecies for each tempereture plateau
                    for j in range(len(start_index)):
                        df = df_data.loc[start_index[j]:end_index[j]]
                        start_indicies.append(start_index[j])
                        end_indicies.append(end_index[j])
                        # calculate min, max and mean of each temperature plateau and pass it into a dictionary
                        df_dict[f"Plataeu_{j+1}"] = sum_channel_stats(df, channels, f"Plataeu_{j+1}")
                        plateau_list = start_index
            
            except (pd.errors.ParserError, TypeError) as e:
                print(f"Error processing {data_file}")
                print(e)
                pass
            
            #concatonate the dfs into a single dataframe
            df_main = pd.concat(df_dict.values(), axis=1)
            if not os.path.exists(file_path):
                with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
                    df_main.to_excel(writer, sheet_name=data_file)
            else:
                with pd.ExcelWriter(file_path, engine='openpyxl', mode="a", if_sheet_exists='replace') as writer:
                    df_main.to_excel(writer, sheet_name=data_file)
            
            #plot data pending user request  
            if plot_data: 
                plt.figure(figsize=(12,8))
                plt.title(data_file)
                for z in range(len(plateau_list)):
                    for i, ch in enumerate(channels):
                        if start_indicies[z] is not None:
                            plt.plot(df_data["time"], df_data[ch], linewidth=0.5, color=ch_cols[i], alpha=0.5)
                            plt.scatter(df_data["time"], df_data[ch], s=1, label=str(ch), color=ch_cols[i], alpha=0.2)
                            plt.scatter(df_data["time"][start_indicies[z]:end_indicies[z]], df_data[ch][start_indicies[z]:end_indicies[z]], marker='o', facecolors='none', color='red', s = 30, alpha=0.2)    
            if plot_data:
                plt.grid()
                plt.ylim(20,120)
                plt.xlabel("Time (s)")
                plt.ylabel("Temperature (degC)")
                plt.show()
        
       