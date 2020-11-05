## load Parflow output and make plots / do anaylsis

import sys
import os
import numpy as np
import matplotlib.pyplot as plt
from parflowio.pyParflowio import PFData


if len(sys.argv)<4:
    print('Usage: <script> <run_folder> <run_name> <plots_folder>')
    sys.exit(0)
else:
    RUN_FOLDER, RUN_NAME, PLOTS_FOLDER = sys.argv[1:]


def pfread(pfbfile):
    """
    Read a pfb file and return data as an ndarray
    :param pfbfile: path to pfb file
    :return: An ndarray of ndim=3, with shape (nz, ny, nx)
    """
    if not os.path.exists(pfbfile):
        raise RuntimeError(f'{pfbfile} not found')

    pfb_data = PFData(pfbfile)
    pfb_data.loadHeader()
    pfb_data.loadData()
    arr = pfb_data.moveDataArray()
    pfb_data.close()
    assert arr.ndim == 3, 'Only 3D arrays are supported'
    return arr


STOP_TIME = 24 * 365  # hours in a year
# intialize array for data we want to analyze/plot
data = np.zeros([8, STOP_TIME])

# reading the CLM file PFCLM_SC.out.clm_output.<file number>.C.pfb
# variables are by layer:
# 0  total latent heat flux (Wm-2)
# 1  total upward LW radiation (Wm-2)
# 2  total sensible heat flux (Wm-2)
# 3  ground heat flux (Wm-2)
# 4  net veg. evaporation and transpiration and soil evaporation (mms-1)
# 5  ground evaporation (mms-1)
# 6  soil evaporation (mms-1)
# 7  vegetation evaporation (canopy) and transpiration (mms-1)
# 8  transpiration (mms-1)
# 9  infiltration flux (mms-1)
# 10 SWE (mm)
# 11 ground temperature (K)
# 12 irrigation flux
# 13-24 Soil temperature by layer (K)

slope    = 0.05
mannings = 2.e-6


# loop over a year of files and load in the CLM output
# then map specific variables to the data array which holds things for analysis
# and plotting
for i in range(STOP_TIME):
    
    filename = os.path.join(RUN_FOLDER, RUN_NAME + '.out.clm_output.{:05d}.C.pfb'.format(i+1))
    data_arr = pfread(filename)
    
    data[1, i] = data_arr[0, ...]  # total (really, it is net) latent heat flux (Wm-2)
    data[2, i] = data_arr[4, ...]  # net veg. evaporation and transpiration and soil evaporation (mms-1)
    data[3, i] = data_arr[10, ...] # SWE (mm)
    
    filename = os.path.join(RUN_FOLDER, RUN_NAME + '.out.press.{:05d}.pfb'.format(i))
    data_arr = pfread(filename)
    data[4, i] = (np.sqrt(slope)/mannings) * np.maximum(data_arr[-1, ...], 0.0) ** (5/3)

# Plot LH Flux, SWE and Runoff
fig, ax = plt.subplots()
ax.plot(range(STOP_TIME), data[1, ...], color='g')
ax.plot(range(STOP_TIME), data[3, ...], color='b')
ax.set_xlabel('Time, WY [hr]')
ax.set_ylabel('LH Flux, SWE')

ax2 = ax.twinx()
ax2.plot(range(STOP_TIME), data[4, ...], color='r')
ax2.set_ylabel('Runoff [m/h]')

os.makedirs(PLOTS_FOLDER, exist_ok=True)
plt.savefig(os.path.join(PLOTS_FOLDER, 'plot.png'), bbox_inches='tight')
