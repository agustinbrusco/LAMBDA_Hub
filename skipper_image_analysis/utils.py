from typing import Callable, Optional
import numpy as np
from numpy.typing import ArrayLike
from astropy.io import fits
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap


BLUE_CUBE_CMAP = LinearSegmentedColormap.from_list(
    name="blue_cube",
    colors=["black", "midnightblue", "blue", "steelblue", "slategray", "white"],
)


def get_overscan_from_fits(
    fits_imgs: fits.hdu.hdulist.HDUList,
) -> int:
    return int(fits_imgs[0].header["NCOL"]) - int(fits_imgs[0].header["CCDNCOL"]) // 2


def mask_baseline_error(frame_vals: ArrayLike) -> ArrayLike:
    row_medians = np.median(frame_vals, axis=1)
    median_of_medians = np.median(row_medians)
    mad_of_medians = np.median(np.abs(row_medians - median_of_medians))
    outlier_cond = row_medians < (median_of_medians - 10 * mad_of_medians)
    frame_vals[outlier_cond] = np.nan
    return frame_vals


def plot_ccd_image(
    image: ArrayLike | fits.hdu.hdulist.HDUList,
    cmap: Optional[str] = None,
    remove_overscan: Optional[bool] = True,
    orientation: Optional[str] = "horizontal",
    value_map: Optional[Callable] = None,
) -> tuple[plt.figure, plt.Axes]:
    global BLUE_CUBE_CMAP
    if remove_overscan and isinstance(image, fits.hdu.hdulist.HDUList):
        overscan_pix = get_overscan_from_fits(image) - 8  # PREGUNTAR
        vertical_image = np.block(
            [
                [image[0].data[:, :-overscan_pix], image[1].data[:, -overscan_pix::-1]],
                [image[2].data[:, :-overscan_pix], image[3].data[:, -overscan_pix::-1]],
            ],
        )
    elif isinstance(image, fits.hdu.hdulist.HDUList):
        vertical_image = np.block(
            [
                [image[0].data, image[1].data[:, ::-1]],
                [image[2].data, image[3].data[:, ::-1]],
            ],
        )
    else:
        if remove_overscan:
            raise ValueError(
                "`remove_overscan = True` is only valid when `image` is of type "
                "fits.hdu.hdulist.HDUList."
            )
        vertical_image = np.block(
            [
                [image[0], image[1][:, ::-1]],
                [image[2], image[3][:, ::-1]],
            ],
        )
    if orientation == "horizontal":
        plotted_image = vertical_image.T
    else:
        plotted_image = vertical_image
    if cmap is None:
        cmap = BLUE_CUBE_CMAP
    if value_map is None:
        def value_map(x: ArrayLike) -> ArrayLike:
            return np.log(1 + np.abs(x) / 100)
    fig, ax = plt.subplots(1, 1, )
    ax.imshow(value_map(plotted_image), cmap=cmap)
    ax.axis("off")
    return fig, ax
