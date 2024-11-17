import pandas as pd


"""
@author Tomasz Lasota
@version 1.0

Module for temp_plateau_analysis.py functions.

This module contains utility functions to analyze and summarize temperature stability data, identify distinct plateaus, 
and calculate statistical summaries for given temperature channels.

Functions:
-----------
1. summerise_ch_stats(df: pd.DataFrame, channels: list, plataeu: str) -> pd.DataFrame:
   - Computes minimum, mean, and maximum values for each specified channel in the given DataFrame.
   - Returns a summary DataFrame with calculated statistics.

2. find_distinct_plateaus(df: pd.DataFrame, tolerance: float, num_points: int, channels: list, plateau_threshold: float, step_size: int = 200) -> list:
   - Identifies distinct stable plateaus in the given DataFrame based on stability tolerance and a threshold to differentiate plateaus.
   - Returns a list of DataFrames, each representing the last `num_points` of a distinct plateau.

Usage:
-------
Import the module in your main temp_plateau_analysis.py to access these functions.
"""

def summerise_ch_stats(df: pd.DataFrame, channels:list, plataeu:str) -> pd.DataFrame:
    """
    Computes the minimum, mean, and maximum values for each channel (channles) in the given DataFrame.

    Parameters:
    -----------
    df : pd.DataFrame
        A pandas DataFrame that contains channel data in columns labeled and storred in var channels, and possibly other columns.
        It is assumed that these columns hold numeric data for which statistical summaries (min, mean, max) are needed.
    channels : list
        List of column names aka channels used to created the DataFrame

    Returns:
    --------
    summary_df : pd.DataFrame
        A new DataFrame containing the calculated 'min', 'mean', and 'max' values for each of the channel columns ('ch1', 'ch2', 'ch3', 'ch4').
        The resulting DataFrame has the following structure:
        - Index: The channel names (e.g., 'ch1', 'ch2', 'ch3', 'ch4').
        - Columns: ['min', 'mean', 'max'] with the corresponding statistics for each channel.

    """

    ch_columns = df[channels]
    # Calculate min, mean, and max for each channel
    min_values = ch_columns.min()
    mean_values = ch_columns.mean()
    max_values = ch_columns.max()

    # Combine results into a summary DataFrame
    summary_df = pd.DataFrame({
        f'{plataeu}min': min_values,
        f'{plataeu}mean': mean_values,
        f'{plataeu}max': max_values
    })

    return summary_df


def find_distinct_plateaus(df: pd.DataFrame, 
                           tolerance: float, 
                           num_points: int, 
                           channels: list, 
                           plateau_threshold: float, 
                           step_size: int = 200) -> list:
    """
    Find distinct plateaus and return the last `num_points` of each distinct plateau.

    :param df: DataFrame with temperature channels (e.g., 'ch1', 'ch2', 'ch3', 'ch4').
    :param tolerance: Maximum allowed difference between adjacent points for stability.
    :param num_points: Number of consecutive stable points to extract.
    :param channels: List of temperature channels to analyze.
    :param plateau_threshold: Minimum difference between consecutive plateaus to define distinct plateaus.
    :param step_size: Number of rows to step through during iteration (default is 200).

    :return: A list of DataFrames, each containing the last `num_points` of a distinct plateau.
    """
    plateaus = []  # Store distinct plateaus
    current_plateau = []  # Track the current plateau
    last_plateau_start = None  # Track the end value of the last plateau

    for i in range(0, len(df) - num_points + 1, step_size):
        # Get a segment of 'num_points' rows starting at index 'i'
        segment = df.iloc[i:i + num_points]

        # Check stability: ensure the segment is stable within the tolerance
        is_stable = all(
            (segment[channel].max() - segment[channel].min()) <= tolerance for channel in channels
        )

        if is_stable:
            # Add the entire segment to the current plateau
            current_plateau = segment
        else:
            # If stability breaks and a plateau exists, finalize it
            if len(current_plateau) >= num_points:
                plateau_df = pd.DataFrame(current_plateau)

                # Check if the current plateau is distinct from the last one
                if last_plateau_start is None or abs(plateau_df[channels[0]].iloc[0] - last_plateau_start) >= plateau_threshold:
                    plateaus.append(plateau_df)
                    last_plateau_start = plateau_df[channels[0]].iloc[0]  # Update the end value for comparison

    # Handle the final plateau if it ends with stable data
    if len(current_plateau) >= num_points:
        plateau_df = pd.DataFrame(current_plateau)
        if last_plateau_start is None or abs(plateau_df[channels[0]].iloc[0] - last_plateau_start) >= plateau_threshold:
            plateaus.append(plateau_df)

    return plateaus