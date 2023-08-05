# -*- coding: utf-8 -*-

# BCDI: tools for pre(post)-processing Bragg coherent X-ray diffraction imaging data
#   (c) 07/2017-06/2019 : CNRS UMR 7344 IM2NP
#   (c) 07/2019-present : DESY PHOTON SCIENCE
#       authors:
#         Jerome Carnis, carnis_jerome@yahoo.fr

from numpy.fft import fftshift
import numpy as np
import matplotlib.pyplot as plt
import h5py
import tkinter as tk
from tkinter import filedialog
import sys
sys.path.append('D:/myscripts/bcdi/')
import bcdi.graph.graph_utils as gu

helptext = """
Open and plot the psf from a .cxi reconstruction file (from PyNX). The psf has to be fftshifted.
"""

datadir = "D:/data/P10_August2019_CDI/data/gold_2_2_2_00022/pynx/1000_1000_1000_1_1_1/current_paper/"
save_dir = None
is_orthogonal = True  # True if the data was orthogonalized before phasing
comment = '_binning2x2x2'  # should start with _
width = 30  # the psf will be plotted for +/- this number of pixels from center of the array
vmin = -6  # min of the colorbar for plots (log scale). Use np.nan for default.
vmax = 1  # max of the colorbar for plots (log scale). Use np.nan for default.
save_slices = True  # True to save individual 2D slices (in z, y, x)
tick_direction = 'out'  # 'out', 'in', 'inout'
tick_length = 8  # in plots
tick_width = 2  # in plots
linewidth = 2  # linewidth for the plot frame
###################
# define colormap #
###################
bad_color = '1.0'  # white background
colormap = gu.Colormap(bad_color=bad_color)
my_cmap = colormap.cmap

#####################################################
# load the CXI file, output of PyNX phase retreival #
#####################################################
root = tk.Tk()
root.withdraw()
file_path = filedialog.askopenfilename(initialdir=datadir, filetypes=[("CXI", "*.cxi")])

h5file = h5py.File(file_path, 'r')
try:
    dataset = fftshift(h5file['/entry_1/image_1/instrument_1/detector_1/point_spread_function'].value)
except KeyError as ex:
    print('The PSF was not saved in the CXI file')
    raise KeyError from ex

#########################
# check some parameters #
#########################
save_dir = save_dir or datadir
nbz, nby, nbx = dataset.shape
print(f'psf shape = {dataset.shape}')
cen_z, cen_y, cen_x = nbz // 2, nby // 2, nbx // 2
if any((cen_z-width < 0, cen_z+width > nbz, cen_y-width < 0, cen_y+width > nby, cen_x-width < 0, cen_x+width > nbx)):
    raise ValueError('width is not compatible with the psf shape')
if is_orthogonal:
    title = 'log(psf) in laboratory frame'
else:
    title = 'log(psf) in detector frame'

#########################
# plot and save the psf #
#########################
fig, _, _ = gu.multislices_plot(dataset[cen_z-width:cen_z+width, cen_y-width:cen_y+width, cen_x-width:cen_x+width],
                                scale='log', sum_frames=False, title=title, vmin=vmin, vmax=vmax,
                                reciprocal_space=False, is_orthogonal=is_orthogonal, plot_colorbar=True)
fig.savefig(save_dir + 'psf_centralslice' + comment + '.png')

if save_slices:
    fig, axs, _ = gu.imshow_plot(dataset[cen_z, cen_y-width:cen_y+width, cen_x-width:cen_x+width], sum_frames=False,
                                 scale='log', vmin=vmin, vmax=vmax, reciprocal_space=False, is_orthogonal=is_orthogonal,
                                 plot_colorbar=False)
    axs.tick_params(labelbottom=False, labelleft=False, direction=tick_direction, length=tick_length, width=tick_width)
    axs.spines['right'].set_linewidth(linewidth)
    axs.spines['left'].set_linewidth(linewidth)
    axs.spines['top'].set_linewidth(linewidth)
    axs.spines['bottom'].set_linewidth(linewidth)
    fig.savefig(save_dir + 'psf_centralslice_z' + comment + '.png')

    fig, axs, _ = gu.imshow_plot(dataset[cen_z-width:cen_z+width, cen_y, cen_x-width:cen_x+width], sum_frames=False,
                                 scale='log', vmin=vmin, vmax=vmax, reciprocal_space=False, is_orthogonal=is_orthogonal,
                                 plot_colorbar=False)
    axs.tick_params(labelbottom=False, labelleft=False, direction=tick_direction, length=tick_length, width=tick_width)
    axs.spines['right'].set_linewidth(linewidth)
    axs.spines['left'].set_linewidth(linewidth)
    axs.spines['top'].set_linewidth(linewidth)
    axs.spines['bottom'].set_linewidth(linewidth)
    fig.savefig(save_dir + 'psf_centralslice_y' + comment + '.png')

    fig, axs, plot = gu.imshow_plot(dataset[cen_z-width:cen_z+width, cen_y-width:cen_y+width, cen_x], sum_frames=False,
                                    scale='log', vmin=vmin, vmax=vmax, reciprocal_space=False,
                                    is_orthogonal=is_orthogonal, plot_colorbar=False)
    axs.tick_params(labelbottom=False, labelleft=False, direction=tick_direction, length=tick_length, width=tick_width)
    axs.spines['right'].set_linewidth(linewidth)
    axs.spines['left'].set_linewidth(linewidth)
    axs.spines['top'].set_linewidth(linewidth)
    axs.spines['bottom'].set_linewidth(linewidth)
    fig.savefig(save_dir + 'psf_centralslice_x' + comment + '.png')
    axs.tick_params(labelbottom=True, labelleft=True)
    cbar = plt.colorbar(plot, ax=axs)
    cbar.outline.set_linewidth(linewidth)
    cbar.ax.tick_params(length=tick_length, width=tick_width)
    fig.savefig(save_dir + 'psf_centralslice_x_labels_colorbar' + comment + '.png')
plt.show()
