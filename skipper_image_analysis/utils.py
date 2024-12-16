from typing import Callable, Optional
import numpy as np
from numpy.typing import ArrayLike
from astropy.io import fits
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

GANANCIA = {0: 210, 1: 232, 2: 207, 3: 159}
PRESCAN_PIX = 8

BLUE_CUBE_CMAP = LinearSegmentedColormap.from_list(
    name="blue_cube",
    colors=["black", "midnightblue", "blue", "steelblue", "slategray", "white"],
)


def gaussiana(x, amplitud, mu, sigma):
    return amplitud * np.exp(-((x - mu) ** 2) / (2 * sigma**2))


def get_overscan_from_fits(
    fits_imgs: fits.hdu.hdulist.HDUList,
) -> int:
    return int(fits_imgs[0].header["NCOL"]) - int(fits_imgs[0].header["CCDNCOL"]) // 2


def get_rowcol_ovserscan(
    imgs: fits.hdu.hdulist.HDUList,
) -> tuple[int, int]:
    row_overscan_len = int(imgs[0].header["NROW"]) - int(imgs[0].header["CCDNROW"]) // 2
    col_overscan_len = int(imgs[0].header["NCOL"]) - int(imgs[0].header["CCDNCOL"]) // 2
    col_overscan_len -= 8  # Prescan is considered at NCOL
    return row_overscan_len, col_overscan_len


def correct_overscan(
    imgs: fits.hdu.hdulist.HDUList,
) -> fits.hdu.hdulist.HDUList:
    row_overscan_len, col_overscan_len = get_rowcol_ovserscan(imgs)
    for i, frame in enumerate(imgs):
        imgs[i].data -= np.mean(  # media: os en cols se expone solo en registro serial
            frame.data[:, -col_overscan_len:],
            axis=1,
            keepdims=True,
        )  # Restamos media del overscan en columnas a cada fila.
        imgs[i].data -= np.median(  # mediana: os en filas se expone en área activa
            frame.data[-row_overscan_len:, :],
            axis=0,
            keepdims=True,
        )  # Restamos mediana del overscan en filas a cada columna.
    return imgs


def mask_baseline_error(frame_vals: ArrayLike) -> ArrayLike:
    row_medians = np.median(frame_vals, axis=1)
    median_of_medians = np.median(row_medians)
    mad_of_medians = np.median(np.abs(row_medians - median_of_medians))
    outlier_cond = row_medians < (median_of_medians - 10 * mad_of_medians)
    frame_vals[outlier_cond] = np.nan
    return frame_vals


def frame_coords_to_ccd_coords(
    coord: tuple[int, int], frame_idx: int, CCDNROWS: int, CCDNCOLS: int
) -> tuple[int, int]:
    """Transforma las coordenadas relativas a un frame a las coordenadas de la \
CCD considerando el frame y el overscan.
    """
    x, y = coord
    row = x
    col = y
    if frame_idx in [1, 3]:
        col = CCDNCOLS - y - 1
    if frame_idx in [2, 3]:
        row = CCDNROWS - x - 1
    return row, col


def ccd_coords_to_frame_coords(
    coord: tuple[int, int], frame_idx: int, CCDNROWS: int, CCDNCOLS: int
) -> tuple[int, int]:
    """Transforma las coordenadas relativas a la CCD a las coordenadas de un \
frame considerando el frame y el overscan.
    """
    row, col = coord
    y = col
    x = row
    if frame_idx in [1, 3]:
        y = CCDNCOLS - col - 1
    if frame_idx in [2, 3]:
        x = CCDNROWS - row - 1
    return x, y


def plot_ccd_image(
    image: ArrayLike | fits.hdu.hdulist.HDUList,
    cmap: Optional[str] = None,
    remove_overscan: Optional[bool] = True,
    orientation: Optional[str] = "horizontal",
    value_map: Optional[Callable] = None,
) -> tuple[plt.figure, plt.Axes, plt.cm.ScalarMappable]:
    global BLUE_CUBE_CMAP
    if remove_overscan and isinstance(image, fits.hdu.hdulist.HDUList):
        row_overscan, col_overscan = get_rowcol_ovserscan(image)
        vertical_image = np.block(
            [
                [
                    image[2].data[:-row_overscan, :-col_overscan],
                    image[3].data[:-row_overscan, -col_overscan::-1],
                ],
                [
                    image[0].data[-row_overscan::-1, :-col_overscan],
                    image[1].data[-row_overscan::-1, -col_overscan::-1],
                ],
            ],
        )
    elif isinstance(image, fits.hdu.hdulist.HDUList):
        vertical_image = np.block(
            [
                [image[2].data, image[3].data[:, ::-1]],
                [image[0].data[::-1, :], image[1].data[::-1, ::-1]],
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
                [image[2], image[3][:, ::-1]],
                [image[0][::-1, :], image[1][::-1, ::-1]],
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

    fig, ax = plt.subplots(
        1,
        1,
    )
    imshow_cmap = ax.imshow(value_map(plotted_image), cmap=cmap)
    ax.axis("off")
    return fig, ax, imshow_cmap


def prepare_frame(
    skipper_image: fits.hdu.hdulist.HDUList,
    frame_idx: int,
    remove_row_median: bool = True,
) -> ArrayLike:
    r_overscan, c_overscan = get_rowcol_ovserscan(skipper_image)
    # Extract Read Error from Column Overscan
    overscan_frame = (
        skipper_image[frame_idx].data[:, -c_overscan:] / GANANCIA[frame_idx]
    )  # e⁻
    # Fit Gaussian to Column Overscan Distribution
    charge_frec, charge_bins = np.histogram(
        overscan_frame.flatten(),
        bins=np.linspace(
            overscan_frame.min(),
            # np.min([overscan_frame.max(), -overscan_frame.min()]),
            overscan_frame.max(),
            500,
        ),
        density=True,
    )
    try:  # Try to fit a Gaussian to the distribution
        popt, *_ = curve_fit(
            gaussiana,
            charge_bins[:-1],
            charge_frec,
            p0=[1 / np.sqrt(2 * np.pi * 4), 0, overscan_frame.std()],
        )
        error = np.abs(popt[2])  # e⁻
    except RuntimeError:  # If the fit fails, use the standard deviation and plot
        error = overscan_frame.std()  # e⁻
        # plt.plot(charge_bins[:-1], charge_frec, ".")
        # plt.plot(charge_bins[:-1], gaussiana(charge_bins[:-1], *popt))
        # plt.show()
    # Correct Baseline from Overscan in Rows and Columns
    skipper_image = correct_overscan(skipper_image)  # A.D.U.
    frame = skipper_image[frame_idx].data  # A.D.U.
    frame = frame[1:-r_overscan, PRESCAN_PIX:-c_overscan]  # A.D.U.
    # CALCULAR MEDIANA Y DEVOLVER
    carga_area_activa = frame.flatten() / GANANCIA[frame_idx]  # e⁻
    mediana_carga = np.median(carga_area_activa)  # e⁻
    # borde_inferior = np.quantile(carga_area_activa, 0.005)  # e⁻
    # borde_superior = np.quantile(carga_area_activa, 0.99)  # e⁻
    # ancho_carga = np.std(
    #     carga_area_activa[
    #         (borde_inferior < carga_area_activa) & (carga_area_activa < borde_superior)
    #     ],
    #     ddof=1,
    # )  # e⁻
    if remove_row_median:
        # Remove the median of each row so that the median of the frame is zero
        frame = frame - np.median(frame, axis=1, keepdims=True)  # A.D.U.

    error_lectura = error * np.sqrt(
        1 + 1 / r_overscan + 1 / c_overscan + 1 / frame.shape[1]
    )  # e⁻: Error propagado tras aplicar todas las correcciones
    error_final = np.sqrt(
        # ancho_carga**2
        # mediana_carga  # Poisson Variance == Poisson Mean
        +(error_lectura**2)
    )  # e⁻
    return frame / GANANCIA[frame_idx], mediana_carga, error_final  # e⁻


def filtro_dipolos(
    frame: ArrayLike,
    threshold_factor: float = 4,
    corte_simetria: float = 30,  # %
) -> tuple[list, list, ArrayLike]:
    """Busca dipolos en un frame de la CCD. Para ello, se calcula el producto entre \
cada pixel y su vecino inferior. Si el producto es menor que un umbral negativo, se \
considera que hay un dipolo. Luego, se revisa que el dipolo sea simétrico, es decir, \
que los valores de los pixeles sean similares en magnitud. Si el dipolo es simétrico, \
se agrega a la lista de dipolos encontrados. Finalmente, se devuelve una lista con \
las coordenadas de los dipolos, una máscara con los dipolos encontrados y una lista \
con los valores de los dipolos.

    Parameters:
    -----------

        `frame {ArrayLike}`: Frame de la CCD a analizar. Debe estar en unidades de \
electrones.

        `threshold_factor {float, optional}`: Factor por el que se multiplica al \
ancho de la distribución de carga en la CCD para calcular el umbral de selección. Es \
decir, un dipolo se considera válido si su autocorrelación es menor que \
`-(threshold_factor * ancho_dist)**2`, donde `ancho_dist` es el ancho de la distribución \
de carga en la CCD. Valor por defecto = 3.

        `corte_simetria {float, optional}`: Defaults to 20.

    Returns:
    --------

        `{tuple[list, list, ArrayLike]}`:
    """
    ancho_dist = np.std(
        frame[(frame > np.quantile(frame, 0.005)) & (frame < np.quantile(frame, 0.99))],
        ddof=1,
    )
    threshold = (threshold_factor * ancho_dist) ** 2
    # frame = frame - np.median(frame, axis=1, keepdims=True)  # Resto la mediana
    prod_arr = frame[:-1] * frame[1:]
    val_trampas = []
    coordenadas_trampas = []
    mascara = np.zeros_like(frame)
    for j, col in enumerate(prod_arr.T):  # Recorro las columnas del frame
        for i, val in enumerate(col):  # Recorro los valores de cada columna
            if val < -threshold:
                # Reviso que no esté en el borde del frame
                if (i == 0) or (i == (len(col) - 1)):
                    continue
                else:
                    i_lleno = np.argmax(frame[i - 1 : i + 2, j]) + i - 1
                    i_vacio = np.argmin(frame[i - 1 : i + 2, j]) + i - 1
                if np.abs(i_lleno - i_vacio) == 1:  # Confirmo adyacencia
                    val_1 = frame[i_lleno, j]
                    val_2 = frame[i_vacio, j]
                    diferencia_relativa = np.abs(
                        100
                        * (np.abs(val_1) - np.abs(val_2))
                        / np.max([np.abs(val_1), np.abs(val_2)])
                    )
                    if diferencia_relativa < corte_simetria:  # filtro por simetría
                        coordenadas_trampas.append(((i_lleno, j), (i_vacio, j)))
                        val_trampas.append(np.abs(val_1 - val_2) / 2)
                        mascara[i_lleno, j] = 1
                        mascara[i_vacio, j] = 1
    return coordenadas_trampas, val_trampas, mascara
