import numpy as np
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import netCDF4 as nc
import scipy as sc
import seaborn as sb
import os
import xarray as xr
import tqdm
from tqdm import tqdm, trange
from scipy import ndimage

"""This script walks through the CAO identification algorithm as described
Temperature data is daily mean ERA5 surface temperature over land"""

def define_caos(temp_data_path, out_dir, quantile=0.03): # we use 3rd percentile
    # Ensure 'date' column is in datetime format

    all_means = xr.open_dataset(temp_data_path)
    
    all_means['date'] = pd.to_datetime(all_means['date'])

    # Calculate 'dayofyear'
    all_means['dayofyear'] = all_means['date'].dt.dayofyear

    # Group by 'dayofyear' and calculate the 10th percentile
    grouped = all_means.groupby('dayofyear')
    percentile_03_xr = grouped.quantile(quantile)

    cao = all_means.copy(deep=True)

    # Loop through each day
    for dayofyear in tqdm(all_means['date'].dt.dayofyear):
        # Get the 10th percentile for the corresponding dayofyear
        percentile_doy = percentile_03_xr.sel(dayofyear=dayofyear)
        
        # Mask values less than the 10th percentile and set them to 0 for the current dayofyear
        cao = xr.where(cao['date'].dt.dayofyear == dayofyear, 
                            xr.where(cao < percentile_doy, 0, cao), 
                            cao)

    # creates a binary cao variable for analysis
    cao.to_netcdf(f'{out_dir}/cao_binary.nc')

if __name__ == "__main__":
    temp_data_path = '/path/to/your/temperature_data.nc'
    out_dir = '/path/to/output/directory'
    define_caos(temp_data_path, out_dir)