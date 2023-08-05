# -*- coding: utf-8 -*-

# BCDI: tools for pre(post)-processing Bragg coherent X-ray diffraction imaging data
#   (c) 07/2017-06/2019 : CNRS UMR 7344 IM2NP
#   (c) 07/2019-present : DESY PHOTON SCIENCE
#       authors:
#         Jerome Carnis, carnis_jerome@yahoo.fr

try:
    import hdf5plugin  # for P10, should be imported before h5py or PyTables
except ModuleNotFoundError:
    pass
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import sys
sys.path.append('D:/myscripts/bcdi/')
import bcdi.experiment.experiment_utils as exp
import bcdi.preprocessing.preprocessing_utils as pru
import bcdi.graph.graph_utils as gu

helptext = """
Open a rocking curve data, plot the mask, the monitor and the stack along the first axis.

It is usefull when you want to localize the Bragg peak for ROI determination.

Supported beamlines: ESRF ID01, PETRAIII P10, SOLEIL SIXS, SOLEIL CRISTAL.
"""

scan = 1301
root_folder = "D:/data/SIXS_2019_Ni/"
sample_name = "S"  # string in front of the scan number in the folder name
save_dir = None  # images will be saved here, leave it to None otherwise (default to data directory's parent)
save_mask = False  # set to True to save the mask
debug = False  # True to see more plots
binning = (1, 1, 1)  # binning to apply to the data
# (stacking dimension, detector vertical axis, detector horizontal axis)
###############################
# beamline related parameters #
###############################
beamline = 'SIXS_2019'  # name of the beamline, used for data loading and normalization by monitor
# supported beamlines: 'ID01', 'SIXS_2018', 'SIXS_2019', 'CRISTAL', 'P10', 'NANOMAX'

custom_scan = False  # True for a stack of images acquired without scan, e.g. with ct in a macro (no info in spec file)
custom_images = np.arange(11353, 11453, 1)  # list of image numbers for the custom_scan
custom_monitor = np.ones(len(custom_images))  # monitor values for normalization for the custom_scan
custom_motors = {"eta": np.linspace(16.989, 18.989, num=100, endpoint=False), "phi": 0, "nu": -0.75, "delta": 36.65}
# ID01: eta, phi, nu, delta
# CRISTAL: mgomega, gamma, delta
# P10: om, phi, chi, mu, gamma, delta
# SIXS: beta, mu, gamma, delta

rocking_angle = "inplane"  # "outofplane" or "inplane"
is_series = False  # specific to series measurement at P10
specfile_name = root_folder + 'alias_dict_2020.txt'
# .spec for ID01, .fio for P10, alias_dict.txt for SIXS_2018, not used for CRISTAL and SIXS_2019
# template for ID01: name of the spec file without '.spec'
# template for SIXS_2018: full path of the alias dictionnary 'alias_dict.txt', typically: root_folder + 'alias_dict.txt'
# template for all other beamlines: ''
###############################
# detector related parameters #
###############################
detector = "Maxipix"    # "Eiger2M" or "Maxipix" or "Eiger4M" or 'Merlin'
x_bragg = 134  # horizontal pixel number of the Bragg peak, leave None for automatic detection (using the max)
y_bragg = 162  # vertical pixel number of the Bragg peak, leave None for automatic detection (using the max)
roi_detector = [y_bragg - 100, y_bragg + 100, x_bragg - 100, x_bragg + 100]
# roi_detector = [y_bragg - 168, y_bragg + 168, x_bragg - 140, x_bragg + 140]  # CH5309
# roi_detector = [552, 1064, x_bragg - 240, x_bragg + 240]  # P10 2018
# roi_detector = [y_bragg - 290, y_bragg + 350, x_bragg - 350, x_bragg + 350]  # PtRh Ar
# [Vstart, Vstop, Hstart, Hstop]
# leave None to use the full detector. Use with center_fft='skip' if you want this exact size.
peak_method = 'max'  # Bragg peak determination: 'max', 'com' or 'maxcom'.
high_threshold = 150000  # everything above will be considered as hotpixel
hotpixels_file = ''  # root_folder + 'merlin_mask_190222_14keV.h5'  #
flatfield_file = ''  # root_folder + "flatfield_maxipix_8kev.npz"  #
template_imagefile = 'Pt_ascan_mu_%05d.nxs'
# template for ID01: 'data_mpx4_%05d.edf.gz' or 'align_eiger2M_%05d.edf.gz'
# template for SIXS_2018: 'align.spec_ascan_mu_%05d.nxs'
# template for SIXS_2019: 'spare_ascan_mu_%05d.nxs'
# template for Cristal: 'S%d.nxs'
# template for P10: '_master.h5'
# template for NANOMAX: '%06d.h5'
nb_pixel_x = None  # fix to declare a known detector but with less pixels (e.g. one tile HS), leave None otherwise
nb_pixel_y = None  # fix to declare a known detector but with less pixels (e.g. one tile HS), leave None otherwise
######################
# setup for the plot #
######################
vmin = 0  # min of the colorbar (log scale)
vmax = 6  # max of the colorbar (log scale)
low_threshold = 1  # everthing <= 1 will be set to 0 in the plot
width = None  # [50, 50]  # [vertical, horizontal], leave None for default
# half width in pixels of the region of interest centered on the peak for the plot
##################################
# end of user-defined parameters #
##################################

###################
# define colormap #
###################
bad_color = '1.0'  # white background
colormap = gu.Colormap(bad_color=bad_color)
my_cmap = colormap.cmap
plt.ion()

##############################
# initialize some parameters #
##############################
save_dirname = 'pynxraw'
flatfield = pru.load_flatfield(flatfield_file)
hotpix_array = pru.load_hotpixels(hotpixels_file)

#######################
# Initialize detector #
#######################
kwargs = dict()  # create dictionnary
kwargs['is_series'] = is_series
kwargs['nb_pixel_x'] = nb_pixel_x  # fix to declare a known detector but with less pixels (e.g. one tile HS)
kwargs['nb_pixel_y'] = nb_pixel_y  # fix to declare a known detector but with less pixels (e.g. one tile HS)

detector = exp.Detector(name=detector, template_imagefile=template_imagefile, roi=roi_detector,
                        binning=binning, **kwargs)

####################
# Initialize setup #
####################
setup = exp.Setup(beamline=beamline, rocking_angle=rocking_angle, custom_scan=custom_scan, custom_images=custom_images,
                  custom_monitor=custom_monitor, custom_motors=custom_motors)

########################################
# print the current setup and detector #
########################################
print('\n##############\nSetup instance\n##############')
print(setup)
print('\n#################\nDetector instance\n#################')
print(detector)

########################
# initialize the paths #
########################
setup.init_paths(detector=detector, sample_name=sample_name, scan_number=scan, root_folder=root_folder,
                 save_dir=save_dir, save_dirname=save_dirname, verbose=True, create_savedir=True,
                 specfile_name=specfile_name, template_imagefile=template_imagefile)

logfile = pru.create_logfile(setup=setup, detector=detector, scan_number=scan, root_folder=root_folder,
                             filename=detector.specfile)


#################
# load the data #
#################
data, mask, monitor, frames_logical = pru.load_data(logfile=logfile, scan_number=scan, detector=detector,
                                                    setup=setup, flatfield=flatfield, hotpixels=hotpix_array,
                                                    debugging=debug)

numz, numy, numx = data.shape
print(f'Data shape: ({numz}, {numy}, {numx})')

##########################
# apply photon threshold #
##########################
if high_threshold != 0:
    nb_thresholded = (data > high_threshold).sum()
    mask[data > high_threshold] = 1
    data[data > high_threshold] = 0
    print(f"Applying photon threshold, {nb_thresholded} high intensity pixels masked")

######################################################
# calculate rocking curve and fit it to get the FWHM #
######################################################
if data.ndim == 3:
    tilt, _, _, _ = pru.goniometer_values(frames_logical=frames_logical, logfile=logfile, scan_number=scan,
                                          setup=setup)
    rocking_curve = np.zeros(numz)

    z0, y0, x0 = pru.find_bragg(data, peak_method=peak_method)
    z0 = np.rint(z0).astype(int)
    y0 = np.rint(y0).astype(int)
    x0 = np.rint(x0).astype(int)

    if x_bragg is None:  # Bragg peak position not defined by the user, use the max
        x_bragg = x0
    if y_bragg is None:  # Bragg peak position not defined by the user, use the max
        y_bragg = y0

    peak_int = int(data[z0, y0, x0])
    print(f"Bragg peak (indices in the eventually binned ROI) at (z, y, x): {z0}, {y0}, {x0},"
          f" intensity = {peak_int}")

    for idx in range(numz):
        rocking_curve[idx] = data[idx, y_bragg - 50:y_bragg + 50,
                                  x_bragg - 50:x_bragg + 50].sum()
    plot_title = f"Rocking curve for a ROI centered on (y, x): ({y_bragg}, {x_bragg})"

    z0 = np.unravel_index(rocking_curve.argmax(), rocking_curve.shape)[0]

    interpolation = interp1d(tilt, rocking_curve, kind='cubic')
    interp_points = 5 * numz
    interp_tilt = np.linspace(tilt.min(), tilt.max(), interp_points)
    interp_curve = interpolation(interp_tilt)
    interp_fwhm = len(np.argwhere(interp_curve >= interp_curve.max() / 2)) * \
                     (tilt.max() - tilt.min()) / (interp_points - 1)
    print(f'FWHM by interpolation = {interp_fwhm:.3f} deg')

    _, (ax0, ax1) = plt.subplots(2, 1, sharex='col', figsize=(10, 5))
    ax0.plot(tilt, rocking_curve, '.')
    ax0.plot(interp_tilt, interp_curve)
    ax0.set_ylabel('Integrated intensity')
    ax0.legend(('data', 'interpolation'))
    ax0.set_title(plot_title)
    ax1.plot(tilt, np.log10(rocking_curve), '.')
    ax1.plot(interp_tilt, np.log10(interp_curve))
    ax1.set_xlabel('Rocking angle (deg)')
    ax1.set_ylabel('Log(integrated intensity)')
    ax0.legend(('data', 'interpolation'))
    plt.pause(0.1)

    # apply low threshold
    data[data <= low_threshold] = 0
    # data = data[data.shape[0]//2, :, :]  # select the first frame e.g. for detector mesh scan
    data = data.sum(axis=0)  # concatenate along the axis of the rocking curve
    title = f'data.sum(axis=0)   peak method={peak_method}\n'
else:  # 2D
    _, y0, x0 = pru.find_bragg(data, peak_method=peak_method)
    peak_int = int(data[y0, x0])
    print(f"Bragg peak (indices in the eventually binned ROI) at (y, x): {y0}, {x0},"
          f" intensity = {peak_int}")
    # apply low threshold
    data[data <= low_threshold] = 0
    title = f'peak method={peak_method}\n'

######################################################################################
# cehck the width parameter for plotting the region of interest centered on the peak #
######################################################################################
if width is None:
    width = [y0, numy-y0, x0, numx-x0]  # plot the full range
else:
    width = [min(width[0], y0, numy-y0), min(width[0], y0, numy-y0),
             min(width[1], x0, numx-x0), min(width[1], x0, numx-x0)]
print(f'width for plotting: {width}')

############################################
# plot mask, monitor and concatenated data #
############################################
if save_mask:
    np.savez_compressed(detector.savedir + 'hotpixels.npz', mask=mask)

gu.combined_plots(tuple_array=(monitor, mask), tuple_sum_frames=False, tuple_sum_axis=(0, 0),
                  tuple_width_v=None, tuple_width_h=None, tuple_colorbar=(True, False), tuple_vmin=np.nan,
                  tuple_vmax=np.nan, tuple_title=('monitor', 'mask'), tuple_scale='linear', cmap=my_cmap,
                  ylabel=('Counts (a.u.)', ''))

max_y, max_x = np.unravel_index(abs(data).argmax(), data.shape)
print(f"Max of the concatenated data along axis 0 at (y, x): ({max_y}, {max_x})  Max = {int(data[max_y, max_x])}")

# plot the region of interest centered on the peak
# extent (left, right, bottom, top)
fig, ax = plt.subplots(nrows=1, ncols=1)
plot = ax.imshow(np.log10(data[y0-width[0]:y0+width[1], x0-width[2]:x0+width[3]]), vmin=vmin, vmax=vmax, cmap=my_cmap,
                 extent=[x0-width[2]-0.5, x0+width[3]-0.5, y0+width[1]-0.5, y0-width[0]-0.5])
ax.set_title(f'{title} Peak at (y, x): ({y0},{x0})   Bragg peak value = {peak_int}')
gu.colorbar(plot)
fig.savefig(detector.savedir + f'sum_S{scan}.png')
plt.show()
