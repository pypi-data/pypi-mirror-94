import os
import cv2
import numpy as np
import pandas as pd
from scipy import stats
from plotnine import ggplot, aes, geom_line, scale_x_continuous, scale_color_manual
from plantcv.plantcv import fatal_error
from plantcv.plantcv import params
from plantcv.plantcv import outputs


def analyze_color(rgb_img, mask, hist_plot_type=None, label="default"):
    """Analyze the color properties of an image object
    Inputs:
    rgb_img          = RGB image data
    mask             = Binary mask made from selected contours
    hist_plot_type   = None, 'all', 'rgb','lab' or 'hsv'
    label            = optional label parameter, modifies the variable name of observations recorded

    Returns:
    analysis_image   = histogram output

    :param rgb_img: numpy.ndarray
    :param mask: numpy.ndarray
    :param hist_plot_type: str
    :param label: str
    :return analysis_images: list
    """
    if len(np.shape(rgb_img)) < 3:
        fatal_error("rgb_img must be an RGB image")

    # Mask the input image
    masked = cv2.bitwise_and(rgb_img, rgb_img, mask=mask)
    # Extract the blue, green, and red channels
    b, g, r = cv2.split(masked)
    # Convert the BGR image to LAB
    lab = cv2.cvtColor(masked, cv2.COLOR_BGR2LAB)
    # Extract the lightness, green-magenta, and blue-yellow channels
    l, m, y = cv2.split(lab)
    # Convert the BGR image to HSV
    hsv = cv2.cvtColor(masked, cv2.COLOR_BGR2HSV)
    # Extract the hue, saturation, and value channels
    h, s, v = cv2.split(hsv)

    # Color channel dictionary
    channels = {"b": b, "g": g, "r": r, "l": l, "m": m, "y": y, "h": h, "s": s, "v": v}

    # Histogram plot types
    hist_types = {"ALL": ("b", "g", "r", "l", "m", "y", "h", "s", "v"),
                  "RGB": ("b", "g", "r"),
                  "LAB": ("l", "m", "y"),
                  "HSV": ("h", "s", "v")}

    if hist_plot_type is not None and hist_plot_type.upper() not in hist_types:
        fatal_error("The histogram plot type was " + str(hist_plot_type) +
                    ', but can only be one of the following: None, "all", "rgb", "lab", or "hsv"!')
    # Store histograms, plotting colors, and plotting labels
    histograms = {
        "b": {"label": "blue", "graph_color": "blue",
              "hist": [float(i[0]) for i in cv2.calcHist([channels["b"]], [0], mask, [256], [0, 255])]},
        "g": {"label": "green", "graph_color": "forestgreen",
              "hist": [float(i[0]) for i in cv2.calcHist([channels["g"]], [0], mask, [256], [0, 255])]},
        "r": {"label": "red", "graph_color": "red",
              "hist": [float(i[0]) for i in cv2.calcHist([channels["r"]], [0], mask, [256], [0, 255])]},
        "l": {"label": "lightness", "graph_color": "dimgray",
              "hist": [float(i[0]) for i in cv2.calcHist([channels["l"]], [0], mask, [256], [0, 255])]},
        "m": {"label": "green-magenta", "graph_color": "magenta",
              "hist": [float(i[0]) for i in cv2.calcHist([channels["m"]], [0], mask, [256], [0, 255])]},
        "y": {"label": "blue-yellow", "graph_color": "yellow",
              "hist": [float(i[0]) for i in cv2.calcHist([channels["y"]], [0], mask, [256], [0, 255])]},
        "h": {"label": "hue", "graph_color": "blueviolet",
              "hist": [float(i[0]) for i in cv2.calcHist([channels["h"]], [0], mask, [256], [0, 255])]},
        "s": {"label": "saturation", "graph_color": "cyan",
              "hist": [float(i[0]) for i in cv2.calcHist([channels["s"]], [0], mask, [256], [0, 255])]},
        "v": {"label": "value", "graph_color": "orange",
              "hist": [float(i[0]) for i in cv2.calcHist([channels["v"]], [0], mask, [256], [0, 255])]}
    }

    # Create list of bin labels for 8-bit data
    binval = np.arange(0, 256)

    analysis_image = None
    # Create a dataframe of bin labels and histogram data
    dataset = pd.DataFrame({'bins': binval, 'blue': histograms["b"]["hist"],
                            'green': histograms["g"]["hist"], 'red': histograms["r"]["hist"],
                            'lightness': histograms["l"]["hist"], 'green-magenta': histograms["m"]["hist"],
                            'blue-yellow': histograms["y"]["hist"], 'hue': histograms["h"]["hist"],
                            'saturation': histograms["s"]["hist"], 'value': histograms["v"]["hist"]})

    # Make the histogram figure using plotnine
    if hist_plot_type is not None:
        if hist_plot_type.upper() == 'RGB':
            df_rgb = pd.melt(dataset, id_vars=['bins'], value_vars=['blue', 'green', 'red'],
                             var_name='Color Channel', value_name='Pixels')
            hist_fig = (ggplot(df_rgb, aes(x='bins', y='Pixels', color='Color Channel'))
                        + geom_line()
                        + scale_x_continuous(breaks=list(range(0, 256, 25)))
                        + scale_color_manual(['blue', 'green', 'red'])
                        )

        elif hist_plot_type.upper() == 'LAB':
            df_lab = pd.melt(dataset, id_vars=['bins'],
                             value_vars=['lightness', 'green-magenta', 'blue-yellow'],
                             var_name='Color Channel', value_name='Pixels')
            hist_fig = (ggplot(df_lab, aes(x='bins', y='Pixels', color='Color Channel'))
                        + geom_line()
                        + scale_x_continuous(breaks=list(range(0, 256, 25)))
                        + scale_color_manual(['yellow', 'magenta', 'dimgray'])
                        )

        elif hist_plot_type.upper() == 'HSV':
            df_hsv = pd.melt(dataset, id_vars=['bins'],
                             value_vars=['hue', 'saturation', 'value'],
                             var_name='Color Channel', value_name='Pixels')
            hist_fig = (ggplot(df_hsv, aes(x='bins', y='Pixels', color='Color Channel'))
                        + geom_line()
                        + scale_x_continuous(breaks=list(range(0, 256, 25)))
                        + scale_color_manual(['blueviolet', 'cyan', 'orange'])
                        )

        elif hist_plot_type.upper() == 'ALL':
            s = pd.Series(['blue', 'green', 'red', 'lightness', 'green-magenta',
                           'blue-yellow', 'hue', 'saturation', 'value'], dtype="category")
            color_channels = ['blue', 'yellow', 'green', 'magenta', 'blueviolet',
                              'dimgray', 'red', 'cyan', 'orange']
            df_all = pd.melt(dataset, id_vars=['bins'], value_vars=s, var_name='Color Channel',
                             value_name='Pixels')
            hist_fig = (ggplot(df_all, aes(x='bins', y='Pixels', color='Color Channel'))
                        + geom_line()
                        + scale_x_continuous(breaks=list(range(0, 256, 25)))
                        + scale_color_manual(color_channels)
                        )
        analysis_image = hist_fig
    # Hue values of zero are red but are also the value for pixels where hue is undefined. The hue value of a pixel will
    # be undef. when the color values are saturated. Therefore, hue values of 0 are excluded from the calculations below

    # Calculate the median hue value (median is rescaled from the encoded 0-179 range to the 0-359 degree range)
    hue_median = np.median(h[np.where(h > 0)]) * 2

    # Calculate the circular mean and standard deviation of the encoded hue values
    # The mean and standard-deviation are rescaled from the encoded 0-179 range to the 0-359 degree range
    hue_circular_mean = stats.circmean(h[np.where(h > 0)], high=179, low=0) * 2
    hue_circular_std = stats.circstd(h[np.where(h > 0)], high=179, low=0) * 2

    # Plot or print the histogram
    if hist_plot_type is not None:
        params.device += 1
        if params.debug == 'print':
            hist_fig.save(os.path.join(params.debug_outdir, str(params.device) + '_analyze_color_hist.png'),
                          verbose=False)
        elif params.debug == 'plot':
            print(hist_fig)

    # Store into global measurements
    # RGB signal values are in an unsigned 8-bit scale of 0-255
    rgb_values = [i for i in range(0, 256)]
    # Hue values are in a 0-359 degree scale, every 2 degrees at the midpoint of the interval
    hue_values = [i * 2 + 1 for i in range(0, 180)]
    # Percentage values on a 0-100 scale (lightness, saturation, and value)
    percent_values = [round((i / 255) * 100, 2) for i in range(0, 256)]
    # Diverging values on a -128 to 127 scale (green-magenta and blue-yellow)
    diverging_values = [i for i in range(-128, 128)]

    if hist_plot_type is not None:
        if hist_plot_type.upper() == 'RGB' or hist_plot_type.upper() == 'ALL':
            outputs.add_observation(sample=label, variable='blue_frequencies', trait='blue frequencies',
                                    method='plantcv.plantcv.analyze_color', scale='frequency', datatype=list,
                                    value=histograms["b"]["hist"], label=rgb_values)
            outputs.add_observation(sample=label, variable='green_frequencies', trait='green frequencies',
                                    method='plantcv.plantcv.analyze_color', scale='frequency', datatype=list,
                                    value=histograms["g"]["hist"], label=rgb_values)
            outputs.add_observation(sample=label, variable='red_frequencies', trait='red frequencies',
                                    method='plantcv.plantcv.analyze_color', scale='frequency', datatype=list,
                                    value=histograms["r"]["hist"], label=rgb_values)

        if hist_plot_type.upper() == 'LAB' or hist_plot_type.upper() == 'ALL':
            outputs.add_observation(sample=label, variable='lightness_frequencies', trait='lightness frequencies',
                                    method='plantcv.plantcv.analyze_color', scale='frequency', datatype=list,
                                    value=histograms["l"]["hist"], label=percent_values)
            outputs.add_observation(sample=label, variable='green-magenta_frequencies', trait='green-magenta frequencies',
                                    method='plantcv.plantcv.analyze_color', scale='frequency', datatype=list,
                                    value=histograms["m"]["hist"], label=diverging_values)
            outputs.add_observation(sample=label, variable='blue-yellow_frequencies', trait='blue-yellow frequencies',
                                    method='plantcv.plantcv.analyze_color', scale='frequency', datatype=list,
                                    value=histograms["y"]["hist"], label=diverging_values)

        if hist_plot_type.upper() == 'HSV' or hist_plot_type.upper() == 'ALL':
            outputs.add_observation(sample=label, variable='hue_frequencies', trait='hue frequencies',
                                    method='plantcv.plantcv.analyze_color', scale='frequency', datatype=list,
                                    value=histograms["h"]["hist"][0:180], label=hue_values)
            outputs.add_observation(sample=label, variable='saturation_frequencies', trait='saturation frequencies',
                                    method='plantcv.plantcv.analyze_color', scale='frequency', datatype=list,
                                    value=histograms["s"]["hist"], label=percent_values)
            outputs.add_observation(sample=label, variable='value_frequencies', trait='value frequencies',
                                    method='plantcv.plantcv.analyze_color', scale='frequency', datatype=list,
                                    value=histograms["v"]["hist"], label=percent_values)

    # Always save hue stats
    outputs.add_observation(sample=label, variable='hue_circular_mean', trait='hue circular mean',
                            method='plantcv.plantcv.analyze_color', scale='degrees', datatype=float,
                            value=hue_circular_mean, label='degrees')
    outputs.add_observation(sample=label, variable='hue_circular_std', trait='hue circular standard deviation',
                            method='plantcv.plantcv.analyze_color', scale='degrees', datatype=float,
                            value=hue_circular_std, label='degrees')
    outputs.add_observation(sample=label, variable='hue_median', trait='hue median',
                            method='plantcv.plantcv.analyze_color', scale='degrees', datatype=float,
                            value=hue_median, label='degrees')

    # Store images
    outputs.images.append(analysis_image)

    return analysis_image
