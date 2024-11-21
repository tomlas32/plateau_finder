# Temperature Data Analysis Script

---

## Overview

This script processes and analyzes temperature data from `.txt` files to identify temperature plateaus and summarize channel statistics. It outputs the results into an Excel file, with optional data visualization. The script is highly configurable, allowing users to customize plateau detection parameters, visualization options, and more.

---

## Features

1. **Data Processing**: Reads and processes temperature data from `.txt` files in the working directory.
2. **Synchronization**: Aligns data using specified temperature thresholds.
3. **Plateau Detection**: Identifies stable temperature plateaus based on user-defined tolerances.
4. **Statistics Generation**: Calculates and summarizes channel-specific statistics (min, max, mean) for each plateau.
5. **Excel Export**: Exports results into an Excel file (`summaryYYYY-MM-DD.xlsx`) with each file's data in separate sheets.
6. **Data Visualization (Optional)**: Generates temperature profile plots with highlighted plateau regions.

---

## Requirements

1. **Python Libraries**:
   - `numpy`
   - `pandas`
   - `matplotlib`
   - `openpyxl`

2. **Custom Functions**:
   Ensure the following modules are accessible in the working directory:
   - `temp_analysis.utils.py`: Includes `find_distinct_plateaus` and `summerise_ch_stats` functions.

---

## Usage

1. **Setup**:
   - Clone or download this repository to your local machine.
   - Place the `.txt` files containing temperature data in the working directory.

2. **Configuration**:
   Open the script and modify the following variables as needed:
   - `plot_data`: Set to `True` to enable plotting or `False` to disable.
   - `find_plateaus`: Set to `True` to use automatic plateau detection or `False` to use hardcoded indices.
   - `tolerance`: Adjust this parameter to define stability criteria for plateau detection.
   - `num_points`: Specify the number of points to define a plateau (~30 seconds by default).

3. **Run the Script**:
   Execute the script in a Python environment. The script will:
   - Process all `.txt` files in the current working directory.
   - Identify plateaus and calculate statistics.
   - Save the summarized data into an Excel file.
   - Optionally generate plots for visual analysis.

---

## Output

1. **Excel File**:
   - **Name**: `summaryYYYY-MM-DD.xlsx`
   - **Structure**:
     - Each sheet corresponds to a processed `.txt` file.
     - Includes channel statistics for each plateau.

2. **Plots (if enabled)**:
   - Time-temperature profiles with plateau regions highlighted.

---

## Customization

1. **Plateau Detection**:
   - When `find_plateaus` is enabled, the script uses the `find_distinct_plateaus` function to dynamically detect plateaus.
   - When disabled, the script uses hardcoded indices:
     - **Start**: `[3650, 7150, 10550, 13750, 17250]`
     - **End**: `[4999, 8499, 11899, 15099, 18599]`

---

## Notes

1. Ensure `.txt` files are formatted with columns: `ch1`, `ch2`, `ch3`, `ch4`, and `time`.
2. If using the `find_plateaus` feature, verify the identified plateaus by enabling `plot_data`.
3. For datasets with unstable plateaus, consider increasing the `tolerance` parameter.

---

## Author

**Tomasz Lasota**  
Version: 1.1  
Date: November 21, 2024
