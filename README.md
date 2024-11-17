Temperature Plateau Analysis Scripts

Overview:

This repository contains scripts for processing and analyzing temperature data. The scripts extract temperature plateaus from temperature.txt files, calculate statistical summaries for identified plateaus, 
and optionally generate plots to visualize temperature profiles.

Scripts:

1. temp_plateau_analysis.py
   
Author: Tomasz Lasota

Version: 1.0

This script processes temperature data, identifies plateaus, calculates channel statistics, and exports results to an Excel file.

Key Features:

Reads and processes temperature data from .txt files.
Synchronizes data timing for better comparisons.
Automatically identifies stable temperature plateaus (or uses hardcoded indices).
Exports summarized statistics to an Excel file (summaryYYYY-MM-DD.xlsx).
Optionally plots temperature data with plateau regions highlighted.

User Configurable Settings:

plot_data: Enable/disable plotting of temperature profiles.
find_plateaus: Enable/disable automated plateau detection.
tolerance: Define stability threshold for plateau detection.
Hardcoded indices can be used if automated detection isn't suitable for your data.

Outputs:

Excel file with statistical summaries for all processed data.
Optional plots for visual inspection of temperature plateaus.

2. temp_analysis_utils.py
   
Author: Tomasz Lasota

Version: 1.0

A utility module containing functions for temperature analysis.

Functions:

summerise_ch_stats(df, channels, plateau)

Calculates min, mean, and max for specified temperature channels.
Returns a DataFrame summarizing channel statistics.

find_distinct_plateaus(df, tolerance, num_points, channels, plateau_threshold, step_size=200)

Identifies distinct, stable temperature plateaus based on user-defined parameters.
Returns a list of DataFrames, each representing a stable plateau.


Example Usage

Input File Format

The scripts expect temperature.txt files with the following structure:

Columns: ch1, ch2, ch3, ch4, time

Header rows: Skipped during reading.

Temperature data: Starts at the 6th row.

How to Run

Place your temperature.txt files in the working directory.
Configure the script settings (plot_data, find_plateaus, etc.) as needed.

Run the script:
bash
python temp_plateau_analysis.py  

Results will be saved in an Excel file (summaryYYYY-MM-DD.xlsx) and optionally visualized in plots.

Example Output
Excel Summary: Contains the following for each plateau:

Min, Mean, Max values for all channels.
Each .txt file's data in separate sheets.

Optional Plots:

Time vs. Temperature with plateau regions highlighted.
Notes
Adjust tolerance and plateau_threshold based on data variability.
Review highlighted plateaus in plots to ensure correct identification.


