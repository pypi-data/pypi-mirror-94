# Analyze reflectance signal data in an index

import os
import cv2
import numpy as np
import pandas as pd
from plantcv.plantcv import params
from plantcv.plantcv import outputs
from plantcv.plantcv import plot_image
from plantcv.plantcv import print_image
from plantcv.plantcv import fatal_error
from plotnine import ggplot, aes, geom_line, scale_x_continuous


def analyze_index(index_array, mask, histplot=False, bins=100, min_bin=0, max_bin=1, label="default"):
    """This extracts the hyperspectral index statistics and writes the values  as observations out to
       the Outputs class.

    Inputs:
    index_array  = Instance of the Spectral_data class, usually the output from pcv.hyperspectral.extract_index
    mask         = Binary mask made from selected contours
    histplot     = if True plots histogram of intensity values
    bins         = optional, number of classes to divide spectrum into
    min_bin      = optional, minimum bin value ("auto" or user input minimum value)
    max_bin      = optional, maximum bin value ("auto" or user input maximum value)
    label        = optional label parameter, modifies the variable name of observations recorded



    :param index_array: __main__.Spectral_data
    :param mask: numpy array
    :param histplot: bool
    :param bins: int
    :param max_bin: float, str
    :param min_bin: float, str
    :param label: str
    :return analysis_image: ggplot, None
    """
    params.device += 1

    debug = params.debug
    params.debug = None
    analysis_image = None

    if len(np.shape(mask)) > 2 or len(np.unique(mask)) > 2:
        fatal_error("Mask should be a binary image of 0 and nonzero values.")

    if len(np.shape(index_array.array_data)) > 2:
        fatal_error("index_array data should be a grayscale image.")

    # Mask data and collect statistics about pixels within the masked image
    masked_array = index_array.array_data[np.where(mask > 0)]
    masked_array = masked_array[np.isfinite(masked_array)]

    index_mean = np.nanmean(masked_array)
    index_median = np.nanmedian(masked_array)
    index_std = np.nanstd(masked_array)

    # Set starting point and max bin values
    maxval = max_bin
    b = min_bin

    # Calculate observed min and max pixel values of the masked array
    observed_max = np.nanmax(masked_array)
    observed_min = np.nanmin(masked_array)

    # Auto calculate max_bin if set
    if type(max_bin) is str and (max_bin.upper() == "AUTO"):
        maxval = float(round(observed_max, 8))  # Auto bins will detect maxval to use for calculating labels/bins
    if type(min_bin) is str and (min_bin.upper() == "AUTO"):
        b = float(round(observed_min, 8))  # If bin_min is auto then overwrite starting value

    # Print a warning if observed min/max outside user defined range
    if observed_max > maxval or observed_min < b:
        print("WARNING!!! The observed range of pixel values in your masked index provided is [" + str(observed_min) +
              ", " + str(observed_max) + "] but the user defined range of bins for pixel frequencies is [" + str(b) +
              ", " + str(maxval) + "]. Adjust min_bin and max_bin in order to avoid cutting off data being collected.")

    # Calculate histogram
    hist_val = [float(i[0]) for i in cv2.calcHist([masked_array.astype(np.float32)], [0], None, [bins], [b, maxval])]
    bin_width = (maxval - b) / float(bins)
    bin_labels = [float(b)]
    plotting_labels = [float(b)]
    for i in range(bins - 1):
        b += bin_width
        bin_labels.append(b)
        plotting_labels.append(round(b, 2))

    # Make hist percentage for plotting
    pixels = cv2.countNonZero(mask)
    hist_percent = [(p / float(pixels)) * 100 for p in hist_val]

    params.debug = debug

    if histplot is True:
        dataset = pd.DataFrame({'Index Reflectance': bin_labels,
                                'Proportion of pixels (%)': hist_percent})
        fig_hist = (ggplot(data=dataset,
                           mapping=aes(x='Index Reflectance',
                                       y='Proportion of pixels (%)'))
                    + geom_line(color='red')
                    + scale_x_continuous(breaks=bin_labels, labels=plotting_labels))
        analysis_image = fig_hist
        if params.debug == 'print':
            fig_hist.save(os.path.join(params.debug_outdir,
                                       str(params.device) + index_array.array_type + "hist.png"), verbose=False)
        elif params.debug == 'plot':
            print(fig_hist)

    outputs.add_observation(sample=label, variable='mean_' + index_array.array_type,
                            trait='Average ' + index_array.array_type + ' reflectance',
                            method='plantcv.plantcv.hyperspectral.analyze_index', scale='reflectance', datatype=float,
                            value=float(index_mean), label='none')

    outputs.add_observation(sample=label, variable='med_' + index_array.array_type,
                            trait='Median ' + index_array.array_type + ' reflectance',
                            method='plantcv.plantcv.hyperspectral.analyze_index', scale='reflectance', datatype=float,
                            value=float(index_median), label='none')

    outputs.add_observation(sample=label, variable='std_' + index_array.array_type,
                            trait='Standard deviation ' + index_array.array_type + ' reflectance',
                            method='plantcv.plantcv.hyperspectral.analyze_index', scale='reflectance', datatype=float,
                            value=float(index_std), label='none')

    outputs.add_observation(sample=label, variable='index_frequencies_' + index_array.array_type,
                            trait='index frequencies', method='plantcv.plantcv.analyze_index', scale='frequency',
                            datatype=list, value=hist_percent, label=bin_labels)

    if params.debug == "plot":
        plot_image(masked_array)
    elif params.debug == "print":
        print_image(img=masked_array, filename=os.path.join(params.debug_outdir, str(params.device) +
                                                            index_array.array_type + ".png"))
    # Store images
    outputs.images.append(analysis_image)

    return analysis_image
