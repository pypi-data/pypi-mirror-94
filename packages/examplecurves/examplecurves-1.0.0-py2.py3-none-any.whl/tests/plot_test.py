import examplecurves
from examplecurves.main import plot_curves, make_family_overview_plots


def test_plots():
    """
    Tests just for smooth running the code.
    """

    sample_curves = examplecurves.Static.create("diagonallinear0")
    plot_curves(sample_curves)
    plot_curves(sample_curves, "with title")

    make_family_overview_plots("nonlinear0")