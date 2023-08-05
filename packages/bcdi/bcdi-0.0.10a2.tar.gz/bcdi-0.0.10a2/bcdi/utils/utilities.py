# -*- coding: utf-8 -*-

# BCDI: tools for pre(post)-processing Bragg coherent X-ray diffraction imaging data
#   (c) 07/2017-06/2019 : CNRS UMR 7344 IM2NP
#   (c) 07/2019-present : DESY PHOTON SCIENCE
#       authors:
#         Jerome Carnis, carnis_jerome@yahoo.fr

import os
import ctypes
import h5py
import numpy as np
from scipy.special import erf
from scipy.interpolate import interp1d
from scipy.optimize import curve_fit
from matplotlib import pyplot as plt
import sys
sys.path.append('C:/Users/Jerome/Documents/myscripts/bcdi/')
sys.path.append('D:/myscripts/bcdi/')
import bcdi.graph.graph_utils as gu


def catch_error(exception):
    """
    Callback processing exception in asynchronous multiprocessing.

    :param exception: the arisen exception
    """
    print(exception)


def find_nearest(reference_array, test_values, width=None):
    """
    Find the indices where original_array is nearest to array_values.

    :param reference_array: a 1D array where to look for the nearest values
    :param test_values: a number or a 1D array of numbers to be tested
    :param width: if not None, it will look for the nearest element within the range [x-width/2, x+width/2[
    :return: index or indices from original_array nearest to values of length len(test_values). Returns the index -1
     if there is no nearest neighbour in the range defined by width.
    """
    original_array, test_values = np.asarray(reference_array), np.asarray(test_values)

    if original_array.ndim != 1:
        raise ValueError('original_array should be 1D')
    if test_values.ndim > 1:
        raise ValueError('array_values should be a number or a 1D array')
    if test_values.ndim == 0:
        nearest_index = (np.abs(original_array - test_values)).argmin()
        return nearest_index
    else:
        nb_values = len(test_values)
        nearest_index = np.zeros(nb_values, dtype=int)
        for idx in range(nb_values):
            nearest_index[idx] = (np.abs(original_array - test_values[idx])).argmin()
        if width is not None:
            for idx in range(nb_values):
                if (reference_array[nearest_index[idx]] >= test_values[idx] + width / 2)\
                        or (reference_array[nearest_index[idx]] < test_values[idx] - width / 2):
                    # no neighbour in the range defined by width
                    nearest_index[idx] = -1
    return nearest_index


def fit3d_poly1(x_axis, a, b, c, d):
    """
    Calculate the 1st order polynomial function on points in a 3D gridgiven the polynomial parameters.

    :param x_axis: (3xN) tuple or array of 3D coordinates
    :param a: offset
    :param b: 1st order parameter for the 1st coordinate
    :param c: 1st order parameter for the 2nd coordinate
    :param d: 1st order parameter for the 3rd coordinate
    :return: the 1st order polynomial calculated on x_axis
    """
    return a + b*x_axis[0] + c*x_axis[1] + d*x_axis[2]


def fit3d_poly2(x_axis, a, b, c, d, e, f, g):
    """
    Calculate the 2nd order polynomial function on points in a 3D gridgiven the polynomial parameters.

    :param x_axis: (3xN) tuple or array of 3D coordinates
    :param a: offset
    :param b: 1st order parameter for the 1st coordinate
    :param c: 1st order parameter for the 2nd coordinate
    :param d: 1st order parameter for the 3rd coordinate
    :param e: 2nd order parameter for the 1st coordinate
    :param f: 2nd order parameter for the 2nd coordinate
    :param g: 2nd order parameter for the 3rd coordinate
    :return: the 2nd order polynomial calculated on x_axis
    """
    return a + b*x_axis[0] + c*x_axis[1] + d*x_axis[2] + e*x_axis[0]**2 + f*x_axis[1]**2 + g*x_axis[2]**2


def fit3d_poly3(x_axis, a, b, c, d, e, f, g, h, i, j):
    """
    Calculate the 3rd order polynomial function on points in a 3D gridgiven the polynomial parameters.

    :param x_axis: (3xN) tuple or array of 3D coordinates
    :param a: offset
    :param b: 1st order parameter for the 1st coordinate
    :param c: 1st order parameter for the 2nd coordinate
    :param d: 1st order parameter for the 3rd coordinate
    :param e: 2nd order parameter for the 1st coordinate
    :param f: 2nd order parameter for the 2nd coordinate
    :param g: 2nd order parameter for the 3rd coordinate
    :param h: 3rd order parameter for the 1st coordinate
    :param i: 3th order parameter for the 2nd coordinate
    :param j: 3th order parameter for the 3rd coordinate
    :return: the 3rd order polynomial calculated on x_axis
    """
    return a + b*x_axis[0] + c*x_axis[1] + d*x_axis[2] + e*x_axis[0]**2 + f*x_axis[1]**2 + g*x_axis[2]**2 +\
        h*x_axis[0]**3 + i*x_axis[1]**3 + j*x_axis[2]**3


def fit3d_poly4(x_axis, a, b, c, d, e, f, g, h, i, j, k, l, m):
    """
    Calculate the 4th order polynomial function on points in a 3D grid given the polynomial parameters.

    :param x_axis: (3xN) tuple or array of 3D coordinates
    :param a: offset
    :param b: 1st order parameter for the 1st coordinate
    :param c: 1st order parameter for the 2nd coordinate
    :param d: 1st order parameter for the 3rd coordinate
    :param e: 2nd order parameter for the 1st coordinate
    :param f: 2nd order parameter for the 2nd coordinate
    :param g: 2nd order parameter for the 3rd coordinate
    :param h: 3rd order parameter for the 1st coordinate
    :param i: 3th order parameter for the 2nd coordinate
    :param j: 3th order parameter for the 3rd coordinate
    :param k: 4th order parameter for the 1st coordinate
    :param l: 4th order parameter for the 2nd coordinate
    :param m: 4th order parameter for the 3rd coordinate
    :return: the 4th order polynomial calculated on x_axis
    """
    return a + b*x_axis[0] + c*x_axis[1] + d*x_axis[2] + e*x_axis[0]**2 + f*x_axis[1]**2 + g*x_axis[2]**2 +\
        h*x_axis[0]**3 + i*x_axis[1]**3 + j*x_axis[2]**3 + k*x_axis[0]**4 + l*x_axis[1]**4 + m*x_axis[2]**4


def function_lmfit(params, x_axis, distribution, iterator=0):
    """
    Calculate distribution using by lmfit Parameters.

    :param params: a lmfit Parameters object
    :param x_axis: where to calculate the function
    :param distribution: the distribution to use
    :param iterator: the index of the relevant parameters
    :return: the gaussian function calculated at x_axis positions
    """
    if distribution == 'gaussian':
        amp = params['amp_%i' % (iterator+1)].value
        cen = params['cen_%i' % (iterator+1)].value
        sig = params['sig_%i' % (iterator+1)].value
        return gaussian(x_axis=x_axis, amp=amp, cen=cen, sig=sig)
    elif distribution == 'skewed_gaussian':
        amp = params['amp_%i' % (iterator+1)].value
        loc = params['loc_%i' % (iterator+1)].value
        sig = params['sig_%i' % (iterator+1)].value
        alpha = params['alpha_%i' % (iterator+1)].value
        return skewed_gaussian(x_axis=x_axis, amp=amp, loc=loc, sig=sig, alpha=alpha)
    elif distribution == 'lorentzian':
        amp = params['amp_%i' % (iterator+1)].value
        cen = params['cen_%i' % (iterator+1)].value
        sig = params['sig_%i' % (iterator+1)].value
        return lorentzian(x_axis=x_axis, amp=amp, cen=cen, sig=sig)
    elif distribution == 'pseudovoigt':
        amp = params['amp_%i' % (iterator+1)].value
        cen = params['cen_%i' % (iterator+1)].value
        sig = params['sig_%i' % (iterator+1)].value
        ratio = params['ratio_%i' % (iterator+1)].value
        return pseudovoigt(x_axis, amp=amp, cen=cen, sig=sig, ratio=ratio)
    else:
        raise ValueError(distribution + ' not implemented')

    
def gaussian(x_axis, amp, cen, sig):
    """
    Gaussian line shape.

    :param x_axis: where to calculate the function
    :param amp: the amplitude of the Gaussian
    :param cen: the position of the center
    :param sig: HWHM of the Gaussian
    :return: the Gaussian line shape at x_axis
    """
    return amp*np.exp(-(x_axis-cen)**2/(2.*sig**2))


def in_range(point, extent):
    """
    Return a boolean depending on whether point is in the indices range defined by extent or not.

    :param point: tuple of three integers (z, y, x) representing the voxel indices to be tested
    :param extent: tuple of six integers (z_start, z_stop, y_start, y_stop, x_tart, x_stop) representing the range of
     valid indices
    :return: True if point belongs to extent, False otherwise
    """
    if (extent[0] <= point[0] <= extent[1]) and\
       (extent[2] <= point[1] <= extent[3]) and\
       (extent[4] <= point[2] <= extent[5]):
        return True
    return False


def is_numeric(string):
    """
    Return True is the string represents a number.

    :param string: the string to be checked
    :return: True of False
    """
    try:
        float(string)
        return True
    except ValueError:
        return False


def load_file(file_path, fieldname=None):
    """
    Load a file. In case of .cxi or .h5 file, it will use a default path to the data.
    'fieldname' is used only for .npz files.

    :param file_path: the path of the reconstruction to load. Format supported: .npy .npz .cxi .h5
    :param fieldname: the name of the field to be loaded
    :return: the loaded data and the extension of the file
    """
    _, extension = os.path.splitext(file_path)
    if extension == '.npz':  # could be anything
        if fieldname is None:  # output of PyNX phasing
            npzfile = np.load(file_path)
            dataset = npzfile[list(npzfile.files)[0]]
        else:  # could be anything
            try:
                dataset = np.load(file_path)[fieldname]
                return dataset, extension
            except KeyError:
                npzfile = np.load(file_path)
                dataset = npzfile[list(npzfile.files)[0]]
    elif extension == '.npy':  # could be anything
        dataset = np.load(file_path)
    elif extension == '.cxi':  # output of PyNX phasing
        h5file = h5py.File(file_path, 'r')
        # group_key = list(h5file.keys())[1]
        # subgroup_key = list(h5file[group_key])
        # dataset = h5file['/'+group_key+'/'+subgroup_key[0]+'/data'].value
        dataset = h5file['/entry_1/data_1/data'][()]
    elif extension == '.h5':  # modes.h5
        h5file = h5py.File(file_path, 'r')
        group_key = list(h5file.keys())[0]
        if group_key == 'mask':  # mask object for Nanomax data
            dataset = h5file['/' + group_key][:]
        else:  # modes.h5 file output of PyNX phase retrieval
            subgroup_key = list(h5file[group_key])
            dataset = h5file['/' + group_key + '/' + subgroup_key[0] + '/data'][0]  # select only first mode
    else:
        raise ValueError("File format not supported: can load only '.npy', '.npz', '.cxi' or '.h5' files")

    if fieldname == 'modulus':
        dataset = abs(dataset)
    elif fieldname == 'angle':
        dataset = np.angle(dataset)
    elif fieldname is None:
        pass
    else:
        raise ValueError('"field" parameter settings is not valid')
    return dataset, extension


def lorentzian(x_axis, amp, cen, sig):
    """
    Lorentzian line shape.

    :param x_axis: where to calculate the function
    :param amp: the amplitude of the Lorentzian
    :param cen: the position of the center
    :param sig: HWHM of the Lorentzian
    :return: the Lorentzian line shape at x_axis
    """
    return amp/(sig*np.pi)/(1+(x_axis-cen)**2/(sig**2))


def objective_lmfit(params, x_axis, data, distribution):
    """
    Calculate total residual for fits to several data sets held
    in a 2-D array, and modeled by gaussian functions.

    :param params: a lmfit Parameters object
    :param x_axis: where to calculate the gaussian distribution
    :param data: data to fit
    :param distribution: distribution to use for fitting
    :return: the residuals of the fit of data using the parameters
    """
    if len(data.shape) == 1:  # single dataset
        data = data[np.newaxis, :]
        x_axis = x_axis[np.newaxis, :]
    ndata, nx = data.shape
    resid = 0.0*data[:]
    # make residual per data set
    for idx in range(ndata):
        resid[idx, :] = data[idx, :] - function_lmfit(params=params, iterator=idx, x_axis=x_axis[idx, :],
                                                      distribution=distribution)
    # now flatten this to a 1D array, as minimize() needs
    return resid.flatten()


def line(x_array, a, b):
    """
    Return y values such that y = a*x + b

    :param x_array: a 1D numpy array of length N
    :param a: coefficient for x values
    :param b: constant offset
    :return: an array of length N containing the y values
    """
    return a * x_array + b


def plane(xy_array, a, b, c):
    """
    Return z values such that z = a*x + b*y + c

    :param xy_array: a (2xN) numpy array, x values being the first row and y values the second row
    :param a: coefficient for x values
    :param b:  coefficient for y values
    :param c: constant offset
    :return: an array of length N containing the z values
    """
    return a * xy_array[0, :] + b * xy_array[1, :] + c


def plane_dist(indices, params):
    """
    Calculate the distance of an ensemble of voxels to a plane given by its parameters.

    :param indices: a (3xN) numpy array, x values being the 1st row, y values the 2nd row and z values the 3rd row
    :param params: a tuple of coefficient (a, b, c, d) such that ax+by+cz+d=0
    :return: a array of shape (N,) containing the distance to the plane for each voxel
    """
    distance = np.zeros(len(indices[0]))
    plane_normal = np.array([params[0], params[1], params[2]])  # normal is [a, b, c] if ax+by+cz+d=0
    for point in range(len(indices[0])):
        distance[point] = abs(params[0]*indices[0, point] + params[1]*indices[1, point] + params[2]*indices[2, point] +
                              params[3]) / np.linalg.norm(plane_normal)
    return distance


def plane_fit(indices, label='', threshold=1, debugging=False):
    """
    Fit a plane to the voxels defined by indices.

    :param indices: a (3xN) numpy array, x values being the 1st row, y values the 2nd row and z values the 3rd row
    :param label: int, label of the plane used for the title in the debugging plot
    :param threshold: the fit will be considered as good if the mean distance of the voxels to the plane is smaller than
     this value
    :param debugging: True to see plots
    :return: a tuple of coefficient (a, b, c, d) such that ax+by+cz+d=0, the matrix of covariant values
    """
    valid_plane = True
    indices = np.asarray(indices)
    params3d, pcov3d = curve_fit(plane, indices[0:2, :], indices[2, :])
    std_param3d = np.sqrt(np.diag(pcov3d))
    params = (-params3d[0], -params3d[1], 1, -params3d[2])
    std_param = (std_param3d[0], std_param3d[1], 0, std_param3d[2])

    if debugging:
        _, ax = gu.scatter_plot(np.transpose(indices), labels=('axis 0', 'axis 1', 'axis 2'),
                                title='Points and fitted plane ' + str(label))
        xlim = ax.get_xlim()
        ylim = ax.get_ylim()
        meshx, meshy = np.meshgrid(np.arange(xlim[0], xlim[1] + 1, 1), np.arange(ylim[0], ylim[1] + 1, 1))
        # meshx varies horizontally, meshy vertically
        meshz = plane(np.vstack((meshx.flatten(), meshy.flatten())),
                      params3d[0], params3d[1], params3d[2]).reshape(meshx.shape)
        ax.plot_wireframe(meshx, meshy, meshz, color='k')
        plt.pause(0.1)

    # calculate the mean distance to the fitted plane
    distance = plane_dist(indices=indices, params=params)
    print(f'plane fit using z=a*x+b*y+c: dist.mean()={distance.mean():.2f},  dist.std()={distance.std():.2f}')

    if distance.mean() > threshold and distance.mean() / distance.std() > 1:
        # probably z does not depend on x and y, try to fit  y = a*x + b
        print('z=a*x+b*y+c: z may not depend on x and y')
        params2d, pcov2d = curve_fit(line, indices[0, :], indices[1, :])
        std_param2d = np.sqrt(np.diag(pcov2d))
        params = (-params2d[0], 1, 0, -params2d[1])
        std_param = (std_param2d[0], 0, 0, std_param2d[1])
        if debugging:
            _, ax = gu.scatter_plot(np.transpose(indices), labels=('axis 0', 'axis 1', 'axis 2'),
                                    title='Points and fitted plane ' + str(label))
            xlim = ax.get_xlim()
            zlim = ax.get_zlim()
            meshx, meshz = np.meshgrid(np.arange(xlim[0], xlim[1] + 1, 1), np.arange(zlim[0], zlim[1] + 1, 1))
            meshy = line(x_array=meshx.flatten(), a=params2d[0], b=params2d[1]).reshape(meshx.shape)
            ax.plot_wireframe(meshx, meshy, meshz, color='k')
            plt.pause(0.1)
        # calculate the mean distance to the fitted plane
        distance = plane_dist(indices=indices, params=params)
        print(f'plane fit using y=a*x+b: dist.mean()={distance.mean():.2f},  dist.std()={distance.std():.2f}')

        if distance.mean() > threshold and distance.mean() / distance.std() > 1:
            # probably y does not depend on x, that means x = constant
            print('y=a*x+b: y may not depend on x')
            constant = indices[0, :].mean()
            params = (1, 0, 0, -constant)
            std_param = (0, 0, 0, indices[0, :].std())
            if debugging:
                _, ax = gu.scatter_plot(np.transpose(indices), labels=('axis 0', 'axis 1', 'axis 2'),
                                        title='Points and fitted plane ' + str(label))
                ylim = ax.get_ylim()
                zlim = ax.get_zlim()
                meshy, meshz = np.meshgrid(np.arange(ylim[0], ylim[1] + 1, 1), np.arange(zlim[0], zlim[1] + 1, 1))
                meshx = np.ones(meshy.shape) * constant
                ax.plot_wireframe(meshx, meshy, meshz, color='k')
                plt.pause(0.1)
            # calculate the mean distance to the fitted plane
            distance = plane_dist(indices=indices, params=params)
            print(f'plane fit using x=constant: dist.mean()={distance.mean():.2f},  dist.std()={distance.std():.2f}')

    if distance.mean() > threshold and distance.mean() / distance.std() > 1:
        # probably the distribution of points is not flat
        print('distance.mean() > 1, probably the distribution of points is not flat')
        valid_plane = False
    return params, std_param, valid_plane


def pseudovoigt(x_axis, amp, cen, sig, ratio):
    """
    Pseudo Voigt line shape.

    :param x_axis: where to calculate the function
    :param amp: amplitude of the Pseudo Voigt
    :param cen: position of the center of the Pseudo Voigt
    :param sig: FWHM of the Pseudo Voigt
    :param ratio: ratio of the Gaussian line shape
    :return: the Pseudo Voigt line shape at x_axis
    """
    sigma_gaussian = sig / (2*np.sqrt(2*np.log(2)))
    scaling_gaussian = 1 / (sigma_gaussian * np.sqrt(2*np.pi))  # the Gaussian is normalized
    sigma_lorentzian = sig / 2
    scaling_lorentzian = 1  # the Lorentzian is normalized
    return amp * (ratio * gaussian(x_axis, scaling_gaussian, cen, scaling_gaussian)
                  + (1-ratio) * lorentzian(x_axis, scaling_lorentzian, cen, sigma_lorentzian))


def ref_count(address):
    """
    Get the reference count using ctypes module

    :param address: integer, the memory adress id
    :return: the number of references to the memory address
    """
    return ctypes.c_long.from_address(address).value


def remove_background(array, q_values, avg_background, avg_qvalues, method='normalize'):
    """
    Subtract the average 1D background to the 3D array using q values.

    :param array: the 3D array. It should be sparse for faster calculation.
    :param q_values: tuple of three 1D arrays (qx, qz, qy), q values for the 3D dataset
    :param avg_background: average background data
    :param avg_qvalues: q values for the 1D average background data
    :param method: 'subtract' or 'normalize'
    :return: the 3D background array
    """
    if array.ndim != 3:
        raise ValueError('data should be a 3D array')
    if (avg_background.ndim != 1) or (avg_qvalues.ndim != 1):
        raise ValueError('avg_background and distances should be 1D arrays')

    qx, qz, qy = q_values

    ind_z, ind_y, ind_x = np.nonzero(array)  # if data is sparse, a loop over these indices only will be fast

    if method == 'subtract':
        avg_background[np.isnan(avg_background)] = 0
        interpolation = interp1d(avg_qvalues, avg_background, kind='linear', bounds_error=False, fill_value=np.nan)
        for index in range(len(ind_z)):
            array[ind_z[index], ind_y[index], ind_x[index]] =\
                array[ind_z[index], ind_y[index], ind_x[index]]\
                - interpolation(np.sqrt(qx[ind_z[index]] ** 2 + qz[ind_y[index]] ** 2 + qy[ind_x[index]] ** 2))
    elif method == 'normalize':
        avg_background[np.isnan(avg_background)] = 1
        avg_background[avg_background < 1] = 1
        interpolation = interp1d(avg_qvalues, avg_background, kind='linear', bounds_error=False, fill_value=np.nan)
        for index in range(len(ind_z)):
            array[ind_z[index], ind_y[index], ind_x[index]] =\
                array[ind_z[index], ind_y[index], ind_x[index]]\
                / interpolation(np.sqrt(qx[ind_z[index]] ** 2 + qz[ind_y[index]] ** 2 + qy[ind_x[index]] ** 2))

    array[np.isnan(array)] = 0
    array[array < 0] = 0

    return array


def skewed_gaussian(x_axis, amp, loc, sig, alpha):
    """
    Skewed Gaussian line shape.

    :param x_axis: where to calculate the function
    :param amp: the amplitude of the Gaussian
    :param loc: the location parameter
    :param sig: HWHM of the Gaussian
    :param alpha: the shape parameter
    :return: the skewed Gaussian line shape at x_axis
    """
    return amp*np.exp(-(x_axis-loc)**2/(2.*sig**2))*(1+erf(alpha/np.sqrt(2)*(x_axis-loc)/sig))


def sum_roi(array, roi, debugging=False):
    """
    Sum the array intensities in the defined region of interest.

    :param array: 2D or 3D array. If ndim=3, the region of interest is applied sequentially to each 2D
     frame, the iteration being peformed over the first axis.
    :param roi: [Vstart, Vstop, Hstart, Hstop] region of interest for the sum
    :param debugging: True to see plots
    :return: a number (if array.ndim=2) or a 1D array of length array.shape[0] (if array.ndim=3) of summed intensities
    """
    ndim = array.ndim
    if ndim == 2:
        nby, nbx = array.shape
    elif ndim == 3:
        _, nby, nbx = array.shape
    else:
        raise ValueError('array should be 2D or 3D')

    if not 0 <= roi[0] < roi[1] <= nby:
        raise ValueError('0 <= roi[0] < roi[1] <= nby   expected')
    if not 0 <= roi[2] < roi[3] <= nbx:
        raise ValueError('0 <= roi[2] < roi[3] <= nbx   expected')

    if ndim == 2:
        sum_array = array[roi[0]:roi[1], roi[2]:roi[3]].sum()
    else:  # ndim = 3
        sum_array = np.zeros(array.shape[0])
        for idx in range(array.shape[0]):
            sum_array[idx] = array[idx, roi[0]:roi[1], roi[2]:roi[3]].sum()
        array = array.sum(axis=0)

    if debugging:
        val = array.max()
        array[roi[0]:roi[1], roi[2]:roi[2]+3] = val
        array[roi[0]:roi[1], roi[3]-3:roi[3]] = val
        array[roi[0]:roi[0]+3, roi[2]:roi[3]] = val
        array[roi[1]-3:roi[1], roi[2]:roi[3]] = val
        gu.combined_plots(tuple_array=(array, sum_array), tuple_sum_frames=False, tuple_sum_axis=0,
                          tuple_scale='log', tuple_title=('summed array', 'ROI integrated intensity'),
                          tuple_colorbar=True)
    return sum_array


# if __name__ == "__main__":
#     import numpy as np
#     import matplotlib.pyplot as plt
#     x = np.linspace(-3, 3, num=200)
#     y = np.asarray([skewed_gaussian(point, 1, 0, 1, 3) for point in x])
#     plt.figure()
#     plt.plot(x, y)
#     plt.show()
