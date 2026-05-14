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
from utide import solve 




def read_tidal_data(filename):
    
    # reads data, replaces values containing M, N and T, and sorts data
   
    if not os.path.exists(filename):
        raise FileNotFoundError(f"{filename} not found")


    data = pd.read_csv(
        filename,
        sep=r"\s+",
        skiprows=11,
        names=["Cycle", "Date", "Time", "Sea Level", "Residual"],
        engine="python")

    # Combine the date and time columns into datetime

    data['Datetime'] = pd.to_datetime(data['Date'] + ' ' + data['Time'])


    data.set_index('Datetime', inplace=True)

    data.replace(
        to_replace=".*[MNT]$",
        value={'Sea Level': np.nan},
        regex=True,
        inplace=True)
    

    data['Sea Level'] = pd.to_numeric(
        data['Sea Level'],
        errors='coerce')
    

    return data
    

    
def extract_single_year_remove_mean(year, data):
    
    #extracts data for a specific year and centers the sea level measurements 
    #around a mean
    
    # Check Sea Level column exists
    if "Sea Level" not in data.columns:
        raise ValueError("Data must contain a 'Sea Level' column.")
      
  
    year = str(year)
    year_data = data.loc[year].copy()
      

    if year_data.empty:
        raise ValueError(f"No data found for year {year}.")
     
   
    mean_sea_level = year_data["Sea Level"].mean()
      
 
    year_data["Sea Level"] = year_data["Sea Level"] - mean_sea_level
      
    return year_data
 


def extract_section_remove_mean(start, end, data):

    # function extracts a specific date range from the data and centers the 
    # sea level data by subtracting the mean    

    start = pd.to_datetime(start, format="%Y%m%d")
    end = pd.to_datetime(end, format="%Y%m%d") + pd.Timedelta(hours=23)
    

    year_data = data.loc[start:end].copy()
    year_data["Sea Level"] = year_data["Sea Level"] - year_data["Sea Level"].mean()
    

    return year_data


def join_data(data1, data2):
    
   # function concatenates (merges) the 2 tidal datasets, and orders them chronologically by datetime
    
    if "Sea Level" not in data1.columns or "Sea Level" not in data2.columns:
        return None
        raise ValueError("Both DataFrames must contain a 'Sea Level' column.")

    # Merge the two DFs
    year_data = pd.concat([data1, data2])

    
    year_data.sort_index(inplace=True)

    return year_data

 

def sea_level_rise(data):

    return

def tidal_analysis(data, constituents, start_datetime):


    print(f"Tidal analysis start")

    start_datetime = start_datetime.replace(tzinfo=None)
    print(f"Time start: {start_datetime}")

    time_Change = data.index - start_datetime

    # Recreate absolute datetimes using start_datetime
    time = start_datetime + time_Change

    # Sea level values
    sea_level = data["Sea Level"].values

    # Remove NaNs
    mask = ~np.isnan(sea_level)

    time = time[mask]
    sea_level = sea_level[mask]

    # Perform harmonic analysis
    coef = solve(
        time,
        sea_level,
        lat=57.14325,          # Aberdeen latitude
        constit=constituents,
        method="ols",
        trend=False,
        verbose=False
    )

    # Extract amplitudes and phases
    amp = coef.A
    pha = coef.g

    print(f"Amplitudes: {amp}, Phases: {pha}")

    return amp, pha


       





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
