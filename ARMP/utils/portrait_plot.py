import sys
import matplotlib
import matplotlib.collections as collections
import matplotlib.pyplot as plt
import numpy as np



def metric_plot(
    data,
    xaxis_labels,
    yaxis_labels,
    fig=None,
    ax=None,
    annotate=False,
    annotate_data=None,
    annotate_textcolors=("black", "white"),
    annotate_textcolors_threshold=(-2, 2),
    annotate_fontsize=15,
    annotate_format="{x:.2f}",
    figsize=(12, 10),
    vrange=None,
    xaxis_fontsize=15,
    yaxis_fontsize=15,
    xaxis_tick_labels_top_and_bottom=False,
    xticklabel_rotation=45,
    inner_line_color="k",
    inner_line_width=0.5,
    cmap="RdBu_r",
    cmap_bounds=None,
    cbar_label=None,
    cbar_label_fontsize=15,
    cbar_tick_fontsize=12,
    cbar_kw={},
    colorbar_off=False,
    missing_color="grey",
    invert_yaxis=True,
    box_as_square=False,
    legend_on=False,
    legend_labels=None,
    legend_box_xy=None,
    legend_box_size=None,
    legend_lw=1,
    legend_fontsize=14,
    debug=False,
):
    """
    Parameters
    ----------
    - `data`: 2d numpy array, a list of 2d numpy arrays, or a 3d numpy array (i.e. stacked 2d numpy arrays)
    - `xaxis_labels`: list of strings, labels for xaixs. Number of list element must consistent to x-axis,
                      or 0 (empty list) to turn off xaxis tick labels
    - `yaxis_labels`: list of strings, labels for yaxis. Number of list element must consistent to y-axis,
                      or 0 (empty list) to turn off yaxis tick labels
    - `fig`: `matplotlib.figure` instance to which the portrait plot is plotted.
             If not provided, use current axes or create a new one.  Optional.
    - `ax`: `matplotlib.axes.Axes` instance to which the portrait plot is plotted.
            If not provided, use current axes or create a new one.  Optional.
    - `annotate`: bool, default=False, add annotating text if true,
                  but work only for heatmap style map (i.e., no triangles)
    - `annotate_data`: 2d numpy array, default=None. If None, the image's data is used.  Optional.
    - `annotate_textcolors`: Tuple. A pair of colors for annotation text. Default is ("black", "white")
    - `annotate_textcolors_threshold`: Tuple or float. Value in data units according to which the colors from textcolors are applied. Default=(-2, 2)
    - `annotate_fontsize`: number (int/float), default=15. Font size for annotation
    - `annotate_format`: format for annotate value, default="{x:.2f}"
    - `figsize`: tuple of two numbers (width, height), default=(12, 10), figure size in inches
    - `vrange`: tuple of two numbers, range of value for colorbar.  Optional.
    - `xaxis_fontsize`: number, default=15, font size for xaxis tick labels.  Optional.
    - `yaxis_fontsize`: number, default=15, font size for yaxis tick labels.  Optional.
    - `xaxis_tick_labels_top_and_bottom`: bool, default=False, if true duplicate xaxis tick label to the other side.  Optional.
    - `xticklabel_rotation`: int or float, default=45, degree of angle to rotate x-axis tick label.  Optional
    - `inner_line_color`: string, default="k" (black), color for inner lines (triangle edge lines).  Optional.
    - `inner_line_width`: float, default=0.5, line width for inner lines (triangle edge lines).  Optional.
    - `cmap`: string, default="RdBu_r", name of matplotlib colormap.  Optional.
    - `cmap_bounds`: list of numbers.  If given, discrete colors are applied.  Optional.
    - `cbar_label`: string, default=None, label for colorbar.  Optional.
    - `cbar_label_fontsize`: number, default=15, font size for colorbar labels.  Optional.
    - `cbar_tick_fontsize`: number, default=12, font size for colorbar tick labels.  Optional.
    - `cbar_kw`: A dictionary with arguments to `matplotlib.Figure.colorbar`.  Optional.
    - `colorbar_off`: Trun off colorbar if True.  Optional.
    - `missing_color`: color, default="grey", `matplotlib.axes.Axes.set_facecolor` parameter.  Optional.
    - `invert_yaxis`: bool, default=True, place y=0 at top on the plot.  Optional.
    - `box_as_square`: bool, default=False, make each box as square.  Optional.
    - `legend_on`: bool, default=False, show legend (only for 2 or 4 triangles portrait plot).  Optional.
    - `legend_labels`: list of strings, legend labels for triangls.  Optional.
    - `legend_box_xy`: tuple of numbers, position of legend box's upper-left corner.  Optional.
                       (lower-left if `invert_yaxis=False`), in `axes` coordinate.  Optional.
    - `legend_box_size`: number, size of legend box.  Optional.
    - `legend_lw`: number, line width of legend, default=1.  Optional.
    - `legend_fontsize`: number, font size for legend, default=14.  Optional.
    - `debug`: bool, default=False, if true print more message when running that help debugging.  Optional.

    Return
    ------
    - `fig`: matplotlib component for figure
    - `ax`: matplotlib component for axis
    - `cbar`: matplotlib component for colorbar (returned if colorbar_off=False)
    - `im`: figure handle for customizing common colorbar (returned if colorbar_off=True)

    This function is a simplified version of the PMP portrait_plot()
    """

    # ----------------
    # Prepare plotting
    # ----------------
    data, num_divide = prepare_data(data, xaxis_labels, yaxis_labels, debug=debug)

    if num_divide not in [1, 2, 4]:
        sys.exit("Error: Number of (stacked) array is not 1, 2, or 4.")

    if annotate:
        if annotate_data is None:
            annotate_data = data
            num_divide_annotate = num_divide
        else:
            annotate_data, num_divide_annotate = prepare_data(
                annotate_data, xaxis_labels, yaxis_labels, debug=debug
            )
            if num_divide_annotate != num_divide:
                sys.exit("Error: annotate_data does not have same size as data")

    # ----------------
    # Ready to plot!!
    # ----------------
    if fig is None:
        fig = plt.figure(figsize=figsize)
    if ax is None:
        ax = fig.add_subplot(111)

    ax.set_facecolor(missing_color)

    if vrange is None:
        vmin = np.nanmin(data)
        vmax = np.nanmax(data)
    else:
        vmin = min(vrange)
        vmax = max(vrange)

    # Normalize colorbar
    if cmap_bounds is None:
        norm = matplotlib.colors.Normalize(vmin=vmin, vmax=vmax)
    else:
        cmap = plt.get_cmap(cmap)
        if "extend" in list(cbar_kw.keys()):
            extend = cbar_kw["extend"]
        else:
            extend = "neither"
        norm = matplotlib.colors.BoundaryNorm(cmap_bounds, cmap.N, extend=extend)

    # [1] Heatmap-style portrait plot (no triangles)
    if num_divide == 1:
        ax, im = heatmap(
            data,
            xaxis_labels,
            yaxis_labels,
            ax=ax,
            invert_yaxis=invert_yaxis,
            cmap=cmap,
            edgecolors="k",
            linewidth=0.5,
            norm=norm,
        )
        if annotate:
            if annotate_data is not None:
                if annotate_data.shape != data.shape:
                    sys.exit("Error: annotate_data has different size than data")
            else:
                annotate_data = data
            ax = annotate_heatmap(
                im,
                ax=ax,
                data=data,
                annotate_data=annotate_data,
                valfmt=annotate_format,
                textcolors=annotate_textcolors,
                threshold=annotate_textcolors_threshold,
                fontsize=annotate_fontsize,
            )


    # X-axis tick labels
    if xaxis_tick_labels_top_and_bottom:
        # additional x-axis tick labels
        ax.tick_params(axis="x", bottom=True, top=True, labelbottom=True, labeltop=True)
    else:
        # Let the horizontal axes labeling appear on top.
        ax.tick_params(top=True, bottom=False, labeltop=True, labelbottom=False)

    """
    # Rotate the tick labels and set their alignment.
    plt.setp(
        ax.get_xticklabels(),
        fontsize=xaxis_fontsize,
        rotation=-30,
        ha="right",
        rotation_mode="anchor",
    )
    """
    # Rotate and align top ticklabels
    plt.setp(
        [tick.label2 for tick in ax.xaxis.get_major_ticks()],
        rotation=xticklabel_rotation,
        ha="left",
        va="center",
        rotation_mode="anchor",
        fontsize=xaxis_fontsize,
    )

    if xaxis_tick_labels_top_and_bottom:
        # Rotate and align bottom ticklabels
        plt.setp(
            [tick.label1 for tick in ax.xaxis.get_major_ticks()],
            rotation=xticklabel_rotation,
            ha="right",
            va="center",
            rotation_mode="anchor",
            fontsize=xaxis_fontsize,
        )

    # Set font size for yaxis tick labels
    plt.setp(ax.get_yticklabels(), fontsize=yaxis_fontsize)

    # Legend
    if legend_on:
        if legend_labels is None:
            sys.exit("Error: legend_labels was not provided.")
        else:
            add_legend(
                num_divide,
                ax,
                legend_box_xy,
                legend_box_size,
                labels=legend_labels,
                lw=legend_lw,
                fontsize=legend_fontsize,
            )

    if box_as_square:
        ax.set_aspect("equal")


    print("im = ", im)
    if not colorbar_off:
        # Create colorbar
        cbar = ax.figure.colorbar(im, ax=ax, **cbar_kw)

        # Label for colorbar
        if cbar_label is not None:
            if "orientation" in list(cbar_kw.keys()):
                if cbar_kw["orientation"] == "horizontal":
                    rotation = 0
                    ha = "center"
                    va = "top"
                    cbar.ax.set_xlabel(
                        cbar_label,
                        rotation=rotation,
                        ha=ha,
                        va=va,
                        fontsize=cbar_label_fontsize,
                    )
                else:
                    rotation = -90
                    ha = "center"
                    va = "bottom"
                    cbar.ax.set_ylabel(
                        cbar_label,
                        rotation=rotation,
                        ha=ha,
                        va=va,
                        fontsize=cbar_label_fontsize,
                    )
            else:
                rotation = -90
                ha = "center"
                va = "bottom"
                cbar.ax.set_ylabel(
                    cbar_label,
                    rotation=rotation,
                    ha=ha,
                    va=va,
                    fontsize=cbar_label_fontsize,
                )
            cbar.ax.tick_params(labelsize=cbar_tick_fontsize)
        return fig, ax, im, cbar
    else:
        return fig, ax, im


# ======================================================================
# Prepare data
# ----------------------------------------------------------------------
def prepare_data(data, xaxis_labels, yaxis_labels, debug=False):
    # In case data was given as list of arrays, convert it to numpy (stacked) array
    if isinstance(data, list):
        if debug:
            print("data type is list")
            print("len(data):", len(data))
        if len(data) == 1:  # list has only 1 array as element
            if isinstance(data[0], np.ndarray) and (len(data[0].shape) == 2):
                data = data[0]
                num_divide = 1
            else:
                sys.exit("Error: Element of given list is not in np.ndarray type")
        else:  # list has more than 1 arrays as elements
            data = np.stack(data)
            num_divide = len(data)

    # Now, data is expected to be be a numpy array (whether given or converted from list)
    if debug:
        print("data.shape:", data.shape)

    if data.shape[-1] != len(xaxis_labels) and len(xaxis_labels) > 0:
        sys.exit("Error: Number of elements in xaxis_label mismatchs to the data")

    if data.shape[-2] != len(yaxis_labels) and len(yaxis_labels) > 0:
        sys.exit("Error: Number of elements in yaxis_label mismatchs to the data")

    if isinstance(data, np.ndarray):
        # data = np.squeeze(data)
        if len(data.shape) == 2:
            num_divide = 1
        elif len(data.shape) == 3:
            num_divide = data.shape[0]
        else:
            print("data.shape:", data.shape)
            sys.exit("Error: data.shape is not right")
    else:
        sys.exit("Error: Converted or given data is not in np.ndarray type")

    if debug:
        print("num_divide:", num_divide)

    return data, num_divide


# ======================================================================
# Portrait plot 1: heatmap-style (no triangle)
# (Inspired from: https://matplotlib.org/devdocs/gallery/images_contours_and_fields/image_annotated_heatmap.html)
# ----------------------------------------------------------------------
def heatmap(data, xaxis_labels, yaxis_labels, ax=None, invert_yaxis=False, **kwargs):
    """
    Create a heatmap from a numpy array and two lists of labels.

    Parameters
    ----------
    data
        A 2D numpy array of shape (M, N).
    yaxis_labels
        A list or array of length M with the labels for the rows.
    xaxis_labels
        A list or array of length N with the labels for the columns.
    ax
        A `matplotlib.axes.Axes` instance to which the heatmap is plotted.  If
        not provided, use current axes or create a new one.  Optional.
    invert_yaxis
        A bool to decide top-down or bottom-up order on y-axis
    **kwargs
        All other arguments are forwarded to `imshow`.
    """

    if ax is None:
        ax = plt.gca()

    if invert_yaxis:
        ax.invert_yaxis()

    # Plot the heatmap
    im = ax.pcolormesh(data, **kwargs)

    # Show all ticks and label them with the respective list entries.
    ax.set_xticks(np.arange(data.shape[1]) + 0.5, minor=False)
    ax.set_yticks(np.arange(data.shape[0]) + 0.5, minor=False)
    ax.set_xticklabels(xaxis_labels)
    ax.set_yticklabels(yaxis_labels)
    ax.tick_params(which="minor", bottom=False, left=False)

    return ax, im


def annotate_heatmap(
    im,
    ax,
    data=None,
    annotate_data=None,
    valfmt="{x:.2f}",
    textcolors=("black", "white"),
    threshold=None,
    **textkw,
):
    """
    A function to annotate a heatmap.

    Parameters
    ----------
    im
        The AxesImage to be labeled.
    ax
        Matplotlib axis
    data
        Data used to color in the image.  If None, the image's data is used.  Optional.
    annotate_data
        Data used to annotate.  If None, the image's data is used.  Optional.
    valfmt
        The format of the annotations inside the heatmap.  This should either
        use the string format method, e.g. "$ {x:.2f}", or be a
        `matplotlib.ticker.Formatter`.  Optional.
    textcolors
        A pair of colors.  The first is used for values below a threshold,
        the second for those above.  Optional.
    threshold
        Value in data units according to which the colors from textcolors are
        applied.  If None (the default) uses the middle of the colormap as
        separation.  Optional.
    **kwargs
        All other arguments are forwarded to each call to `text` used to create
        the text labels.
    """
    if not isinstance(data, (list, np.ndarray)):
        data = im.get_array().reshape(im._meshHeight, im._meshWidth)

    if annotate_data is None:
        annotate_data = data

    if threshold is None:
        threshold = (data.max()) / 2.0

    # Set default alignment to center, but allow it to be
    # overwritten by textkw.
    kw = dict(horizontalalignment="center", verticalalignment="center")
    kw.update(textkw)

    # Get the formatter in case a string is supplied
    if isinstance(valfmt, str):
        valfmt = matplotlib.ticker.StrMethodFormatter(valfmt)

    # Loop over the data and create a `Text` for each "pixel".
    # Change the text's color depending on the data.
    texts = []
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            if type(threshold) is tuple:
                kw.update(
                    color=textcolors[
                        int(
                            (data[i, j] > max(threshold))
                            or (data[i, j] < min(threshold))
                        )
                    ]
                )
            else:
                kw.update(color=textcolors[int(data[i, j] > threshold)])
            text = ax.text(j + 0.5, i + 0.5, valfmt(annotate_data[i, j], None), **kw)
            texts.append(text)

    return ax


# ======================================================================
# Portrait plot legend (four/two triangles)
# ======================================================================
def add_legend(
    num_divide, ax, box_xy=None, box_size=None, labels=None, lw=1, fontsize=14
):
    if box_xy is None:
        box_x = ax.get_xlim()[1] * 1.25
        box_y = ax.get_ylim()[1]
    else:
        # Convert axes coordinate to data coordinate
        # Ref: https://matplotlib.org/stable/tutorials/advanced/transforms_tutorial.html
        box_x, box_y = ax.transLimits.inverted().transform(box_xy)

    if box_size is None:
        box_size = 1.5

    if num_divide == 4:
        if labels is None:
            labels = ["TOP", "RIGHT", "BOTTOM", "LEFT"]
        ax.add_patch(
            plt.Polygon(
                [
                    [box_x, box_y],
                    [box_x + box_size / 2.0, box_y + box_size / 2],
                    [box_x + box_size, box_y],
                ],
                color="k",
                fill=False,
                clip_on=False,
                lw=lw,
            )
        )
        ax.add_patch(
            plt.Polygon(
                [
                    [box_x + box_size, box_y],
                    [box_x + box_size / 2.0, box_y + box_size / 2],
                    [box_x + box_size, box_y + box_size],
                ],
                color="k",
                fill=False,
                clip_on=False,
                lw=lw,
            )
        )
        ax.add_patch(
            plt.Polygon(
                [
                    [box_x + box_size, box_y + box_size],
                    [box_x + box_size / 2.0, box_y + box_size / 2],
                    [box_x, box_y + box_size],
                ],
                color="k",
                fill=False,
                clip_on=False,
                lw=lw,
            )
        )
        ax.add_patch(
            plt.Polygon(
                [
                    [box_x, box_y],
                    [box_x + box_size / 2.0, box_y + box_size / 2],
                    [box_x, box_y + box_size],
                ],
                color="k",
                fill=False,
                clip_on=False,
                lw=lw,
            )
        )
        ax.text(
            box_x + box_size * 0.5,
            box_y + box_size * 0.2,
            labels[0],
            ha="center",
            va="center",
            fontsize=fontsize,
        )
        ax.text(
            box_x + box_size * 0.8,
            box_y + box_size * 0.5,
            labels[1],
            ha="center",
            va="center",
            fontsize=fontsize,
        )
        ax.text(
            box_x + box_size * 0.5,
            box_y + box_size * 0.8,
            labels[2],
            ha="center",
            va="center",
            fontsize=fontsize,
        )
        ax.text(
            box_x + box_size * 0.2,
            box_y + box_size * 0.5,
            labels[3],
            ha="center",
            va="center",
            fontsize=fontsize,
        )
    elif num_divide == 2:
        if labels is None:
            labels = ["UPPER", "LOWER"]
        ax.add_patch(
            plt.Polygon(
                [[box_x, box_y], [box_x, box_y + box_size], [box_x + box_size, box_y]],
                color="k",
                fill=False,
                clip_on=False,
                lw=lw,
            )
        )
        ax.add_patch(
            plt.Polygon(
                [
                    [box_x + box_size, box_y + box_size],
                    [box_x, box_y + box_size],
                    [box_x + box_size, box_y],
                ],
                color="k",
                fill=False,
                clip_on=False,
                lw=lw,
            )
        )
        ax.text(
            box_x + box_size * 0.05,
            box_y + box_size * 0.2,
            labels[0],
            ha="left",
            va="center",
            fontsize=fontsize,
        )
        ax.text(
            box_x + box_size * 0.95,
            box_y + box_size * 0.8,
            labels[1],
            ha="right",
            va="center",
            fontsize=fontsize,
        )
