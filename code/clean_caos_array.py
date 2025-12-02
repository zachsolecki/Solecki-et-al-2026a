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

def clean_up_caos_array(cao_binary, area_threshold=2000, depth_threshold=5):
    # convert from dataarray to numpy format
    da = xr.open_dataarray(cao_binary)
    binary_mask = da.to_numpy()

    labels, num_features = ndimage.label(binary_mask)

    depths = []

    for label in tqdm(range(1, num_features + 1)):
        indices = np.where(labels == label)
        if indices[0].size > 0:
            depth = np.max(indices[0]) - np.min(indices[0]) + 1
            depths.append(depth)
            if depth < 5:
                labels[indices] = 0

    binary_mask = np.where(labels != 0, 1, 0)
    labels, num_features = ndimage.label(binary_mask)

    area_threshold = 2000  # Replace with your desired threshold

    # Iterate through each labeled feature
    for label in tqdm(range(1, num_features + 1)):  # Start from 1 as 0 is background label
        # Find the indices where the labeled feature is present
        indices = np.where(labels == label)

        # Iterate through each slice in the first dimension (x)
        for x in range(min(indices[0]) + 1, max(indices[0])):
            # Extract the 2D slice along the y and z axes
            slice_values = binary_mask[x, indices[1], indices[2]]

            # Calculate the area of the slice for the specific labeled feature
            slice_area = np.sum(slice_values)

            # Check if the area is below the threshold
            if slice_area < area_threshold:
                # Set all values in the slice to 0
                binary_mask[x, indices[1], indices[2]] = 0

    labels, num_features = ndimage.label(binary_mask)
    num_features

    for label in tqdm(range(1, num_features + 1)):
        indices = np.where(labels == label)
        if indices[0].size > 0:
            depth = np.max(indices[0]) - np.min(indices[0]) + 1
            if depth < 5:
                binary_mask[indices] = 0

    np.save('final_binary.npy', binary_mask)

if __name__ == "__main__":
    clean_up_caos_array()