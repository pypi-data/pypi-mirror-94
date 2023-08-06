from examplecurves.main import LoadsLinearCurves


def test_LoadLinearCurves():
    """
    >>> sample_loader = test_LoadLinearCurves()
    >>> sample_loader
    LoadsLinearCurves(verticallinear0)
    >>> sample_loader.get_offset_count()
    0
    >>> sample_loader.iter_curve_creation_parameters([1])
    [{'end_point': [1.0062162844399298, 10.013708464796172], 'curve_length': 5}]
    >>> sample_loader.get_offsets(0)
    Traceback (most recent call last):
    ...
    IndexError: The family of curves has no offsets defined.
    >>> sample_loader.get_offsets(1)
    Traceback (most recent call last):
    ...
    IndexError: The requested index is out of bound of the available offsets.
    """
    specific_sample_loader = LoadsLinearCurves(family_name="verticallinear0")
    return specific_sample_loader