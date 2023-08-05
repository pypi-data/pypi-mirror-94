# -*- coding: utf-8 -*-

# BCDI: tools for pre(post)-processing Bragg coherent X-ray diffraction imaging data
#   (c) 07/2017-06/2019 : CNRS UMR 7344 IM2NP
#   (c) 07/2019-present : DESY PHOTON SCIENCE
#       authors:
#         Jerome Carnis, carnis_jerome@yahoo.fr

import numpy as np
import gc
import matplotlib.pyplot as plt
import sys
import tkinter as tk
from tkinter import filedialog
sys.path.append('D:/myscripts/bcdi/')
import bcdi.utils.utilities as util
import bcdi.graph.graph_utils as gu
import bcdi.postprocessing.postprocessing_utils as pu

helptext = """
Crop a stacked 3D dataset saved in NPZ format, to the desired region of interest.
"""

scan = 22  # scan number, used in the filename when saving
datadir = "D:/data/P10_August2019_CDI/test/gold_2_2_2_00022/pynx/"
crop_center = [250, 250, 250]  # center of the region of interest
roi_size = (100, 100, 100)  # size of the region of interest to crop centered on crop_center, before binning
binning = (1, 1, 1)  # binning to apply further to the cropped data
load_mask = True  # True to load the mask and crop it
load_qvalues = True  # True to load the q values and crop it
is_orthogonal = True  # True if the data is in an orthogonal frame, only used for plots
reciprocal_space = True  # True if the data is in reciprocal space, only used for plots
debug = True  # True to see more plots
comment = '_combined'  # should start with _
##################################
# end of user-defined parameters #
##################################

###################
# define colormap #
###################
colormap = gu.Colormap()
my_cmap = colormap.cmap

#################
# load the data #
#################
root = tk.Tk()
root.withdraw()
file_path = filedialog.askopenfilename(initialdir=datadir, title="Select the data file",
                                       filetypes=[("NPZ", "*.npz"), ("CXI", "*.cxi"), ("HDF5", "*.h5")])
data, _ = util.load_file(file_path)
data = data.astype(float)
nbz, nby, nbx = data.shape

#################################################################
# check parameters depending on the shape of the reference scan #
#################################################################
crop_center = list(crop_center or [nbz // 2, nby // 2, nbx // 2])  # if None, default to the middle of the array
assert len(crop_center) == 3, 'crop_center should be a list or tuple of three indices'
assert np.all(np.asarray(crop_center)-np.asarray(roi_size)//2 >= 0), 'crop_center incompatible with roi_size'
assert crop_center[0]+roi_size[0]//2 <= nbz and crop_center[1]+roi_size[1]//2 <= nby\
        and crop_center[2]+roi_size[2]//2 <= nbx, 'crop_center incompatible with roi_size'

#######################################################
# crop the data, and optionally the mask and q values #
#######################################################
data = pu.crop_pad(data, output_shape=roi_size, crop_center=crop_center, debugging=debug)
data = pu.bin_data(data, binning=binning, debugging=debug)
comment = f'{data.shape[0]}_{data.shape[0]}_{data.shape[0]}_{binning[0]}_{binning[1]}_{binning[2]}' + comment
np.savez_compressed(datadir + 'S' + str(scan) + '_pynx' + comment + '.npz', data=data)

fig, _, _ = gu.multislices_plot(data, sum_frames=True, scale='log', plot_colorbar=True, vmin=0,
                                title='Cropped data', is_orthogonal=is_orthogonal,
                                reciprocal_space=reciprocal_space)
fig.savefig(datadir + 'S' + str(scan) + '_pynx' + comment + '.png')
plt.close(fig)
del data
gc.collect()

if load_mask:
    file_path = filedialog.askopenfilename(initialdir=datadir, title="Select the mask file",
                                           filetypes=[("NPZ", "*.npz"), ("CXI", "*.cxi"), ("HDF5", "*.h5")])
    mask, _ = util.load_file(file_path)
    mask = mask.astype(float)
    mask = pu.crop_pad(mask, output_shape=roi_size, crop_center=crop_center, debugging=debug)
    mask = pu.bin_data(mask, binning=binning, debugging=debug)

    mask[np.nonzero(mask)] = 1
    mask = mask.astype(int)
    np.savez_compressed(datadir + 'S' + str(scan) + '_maskpynx' + comment + '.npz', mask=mask)
    fig, _, _ = gu.multislices_plot(mask, sum_frames=True, scale='linear', plot_colorbar=True, vmin=0,
                                    title='Cropped mask', is_orthogonal=is_orthogonal,
                                    reciprocal_space=reciprocal_space)
    fig.savefig(datadir + 'S' + str(scan) + '_maskpynx' + comment + '.png')
    plt.close(fig)
    del mask
    gc.collect()
    
if load_qvalues:
    file_path = filedialog.askopenfilename(initialdir=datadir, title="Select the file containing q values",
                                           filetypes=[("NPZ", "*.npz")])
    q_values = np.load(file_path)
    qx = q_values['qx']  # 1D array
    qy = q_values['qy']  # 1D array
    qz = q_values['qz']  # 1D array
    qx = pu.crop_pad_1d(qx, roi_size[0], crop_center=crop_center[0])  # qx along z
    qy = pu.crop_pad_1d(qy, roi_size[2], crop_center=crop_center[2])  # qy along x
    qz = pu.crop_pad_1d(qz, roi_size[1], crop_center=crop_center[1])  # qz along y

    numz, numy, numx = len(qx), len(qz), len(qy)
    qx = qx[:numz - (numz % binning[0]):binning[0]]  # along z downstream
    qz = qz[:numy - (numy % binning[1]):binning[1]]  # along y vertical
    qy = qy[:numx - (numx % binning[2]):binning[2]]  # along x outboard

    np.savez_compressed(datadir + 'S' + str(scan) + '_qvalues_' + comment + '.npz', qx=qx, qz=qz, qy=qy)

print('End of script')
plt.ioff()
plt.show()
