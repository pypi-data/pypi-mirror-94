import os

import autofit as af
import autogalaxy as ag
import autogalaxy.plot as aplt


def pixel_scale_from_instrument(instrument):
    """
    Returns the pixel scale from an instrument based on real observations.

    These options are representative of SMA interferometry.

    Parameters
    ----------
    instrument : str
        A string giving the resolution of the desired instrument (SMA).
    """
    if instrument in "sma":
        return (0.05, 0.05)
    else:
        raise ValueError("An invalid data_name resolution was entered - ", instrument)


def grid_from_instrument(instrument):
    """
    Returns the grid from an instrument based on real observations.

    These options are representative of SMA interferometry.

    Parameters
    ----------
    instrument : str
        A string giving the resolution of the desired instrument (SMA).
    """

    pixel_scales = pixel_scale_from_instrument(instrument=instrument)

    if instrument in "sma":
        return ag.Grid2DIterate.uniform(
            shape_native=(151, 151), pixel_scales=pixel_scales
        )
    else:
        raise ValueError("An invalid data_name resolution was entered - ", instrument)


def uv_wavelengths_from_instrument(instrument):
    """
    Returns the uv wavelengths from an instrument based on real observations.

    These options are representative of SMA interferometry.

    Parameters
    ----------
    instrument : str
        A string giving the resolution of the desired instrument (SMA).
    """

    uv_wavelengths_path = "{}".format(os.path.dirname(os.path.realpath(__file__)))

    if instrument in "sma":
        uv_wavelengths_path += "/sma"
    else:
        raise ValueError("An invalid data_name resolution was entered - ", instrument)

    return ag.util.array.numpy_array_1d_from_fits(
        file_path=uv_wavelengths_path + "/uv_wavelengths.fits", hdu=0
    )


def simulator_from_instrument(instrument):
    """
    Returns the pixel scale from an instrument based on real observations.

    These options are representative of VRO, Euclid, HST, over-sampled HST and Adaptive Optics image.

    Parameters
    ----------
    instrument : str
        A string giving the resolution of the desired instrument (VRO | Euclid | HST | HST_Up | AO).
    """

    uv_wavelengths = uv_wavelengths_from_instrument(instrument=instrument)
    grid = grid_from_instrument(instrument=instrument)

    if instrument in "sma":
        return ag.SimulatorInterferometer(
            uv_wavelengths=uv_wavelengths,
            exposure_time_map=ag.Array2D.full(
                fill_value=100.0, shape_native=grid.shape_native
            ),
            background_sky_map=ag.Array2D.full(
                fill_value=1.0, shape_native=grid.shape_native
            ),
            noise_sigma=0.01,
        )
    else:
        raise ValueError("An invalid data_name resolution was entered - ", instrument)


def simulate_interferometer_from_instrument(data_name, instrument, galaxies):

    # Simulate the imaging data, remembering that we use a special image which ensures edge-effects don't
    # degrade our modeling of the telescope optics (e.ag. the PSF convolution).

    grid = grid_from_instrument(instrument=instrument)

    simulator = simulator_from_instrument(instrument=instrument)

    # Use the input galaxies to setup a plane, which will generate the image for the simulated imaging data.
    plane = ag.Plane(galaxies=galaxies)

    interferometer = simulator.from_plane_and_grid(plane=plane, grid=grid)

    # Now, lets output this simulated interferometer-simulator to the test_autoarray/simulator folder.
    test_path = "{}/../../".format(os.path.dirname(os.path.realpath(__file__)))

    dataset_path = f"dataset/interferometer/{data_name}/{instrument}"

    interferometer.output_to_fits(
        visibilities_path=path.join(dataset_path, "visibilities.fits"),
        noise_map_path=path.join(dataset_path, "noise_map.fits"),
        uv_wavelengths_path=path.join(dataset_path, "uv_wavelengths.fits"),
        overwrite=True,
    )

    plotter = aplt.MatPlot2D(output=aplt.Output(path=dataset_path, format="png"))
    plotter = aplt.MatPlot2D(output=aplt.Output(path=dataset_path, format="png"))

    aplt.Interferometer.subplot_interferometer(
        interferometer=interferometer, plotter=plotter
    )

    aplt.Interferometer.figures(
        interferometer=interferometer, visibilities=True, plotter=plotter
    )

    aplt.plane.image(plane=plane, grid=grid, plotter=plotter)


def load_test_interferometer(data_name, instrument):

    test_path = "{}/../../".format(os.path.dirname(os.path.realpath(__file__)))

    dataset_path = f"dataset/interferometer/{data_name}/{instrument}"

    return ag.Interferometer.from_fits(
        visibilities_path=path.join(dataset_path, "visibilities.fits"),
        noise_map_path=path.join(dataset_path, "noise_map.fits"),
        uv_wavelengths_path=path.join(dataset_path, "uv_wavelengths.fits"),
    )
