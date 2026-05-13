# import the modules we need
import pandas as pd
import datetime
import os
import numpy as np
import uptide
import pytz
import math
from scipy import stats
import matplotlib.dates as mdates
import argparse



def read_tidal_data(filename):
    
    # Check if the file exists
    if not os.path.exists(filename):
        raise FileNotFoundError(f"{filename} not found")

    # Read the file's data
    # print(f"Reading data from {filename}...")
    data = pd.read_csv(
        filename,
        sep=r"\s+",
        skiprows=11,
        names=["Cycle", "Date", "Time", "Sea Level", "Residual"],
        engine="python")

    # Combine the date and time columns into datetime
    # print("Processing data...")
    data['Datetime'] = pd.to_datetime(data['Date'] + ' ' + data['Time'])
    # print(f"Data read successfully.")

    # Set datetime as index
    data.set_index('Datetime', inplace=True)

    # Replace M, N, T values with NaN
    # print(f"Replacing M, N, T values with NaN.")
    data.replace(
        to_replace=".*[MNT]$",
        value={'Sea Level': np.nan},
        regex=True,
        inplace=True)
    
    # print row 35 to test replacement
    # print(f"Row 35 after replacement: {data.iloc[34]}")

    # Convert Sea Level column to float
    data['Sea Level'] = pd.to_numeric(
        data['Sea Level'],
        errors='coerce')
    
    # print(f"Row 350 to check float is correct: {data.iloc[349]}")

    return data
    

    
def extract_single_year_remove_mean(year, data):

    return 


def extract_section_remove_mean(start, end, data):

    return #year_data


def join_data(data1, data2):
    
   
    # Check that both DFs contain the sea level column
    if "Sea Level" not in data1.columns or "Sea Level" not in data2.columns:
        return None
        raise ValueError("Both DataFrames must contain a 'Sea Level' column.")

    # Merge the two DFs
    data = pd.concat([data1, data2])

    # Sort by the Datetime index
    data.sort_index(inplace=True)

    return data

 

def sea_level_rise(data):

    return

def tidal_analysis(data, constituents, start_datetime):

    return

def get_longest_contiguous_data(data):

    return 


def main(args_list=None):

    parser = argparse.ArgumentParser(
                     prog="UK Tidal analysis",
                     description="Calculate tidal constiuents and RSL from tide gauge data",
                     )

    parser.add_argument("directory",
                    help="the directory containing txt files with data")
    parser.add_argument('-v', '--verbose',
                    action='store_true',
                    default=False,
                    help="Print progress")

    args = parser.parse_args(args_list)
    dirname = args.directory
    verbose = args.verbose

    print("Add your code here to do things!")
    

if __name__ == '__main__':
    main()
