import copy
from abc import ABC, abstractmethod
from collections import namedtuple
from pathlib import Path
import numpy
import numpy as np
from dicthandling import read_from_json_file, ADDRESS_DELIMITER, put_into_json_file
from scipy.interpolate import CubicSpline
from typing import (
    Tuple,
    Iterable,
    Union,
    Dict,
    Optional,
    overload,
    Sequence,
    Generator,
)
from typing import List
from pandas import DataFrame, Series
import pandas
import sys

major, minor, *rest = sys.version_info
if major == 3 and minor == 6:
    try:
        from importlib_resources import path as _get_resource_path
    except ImportError:
        raise ImportError(
            "Could not import `importlib_resources`. For full support of "
            "`examplecurves` within python 3.6 you need to install "
            "`importlib_resources`."
        )
else:
    from importlib.resources import path as _get_resource_path


def get_resource_path(resource_name):
    with _get_resource_path("examplecurves.resources", resource_name) as retrieved_path:
        potential_path = retrieved_path
    filepath_not_found = potential_path is None
    if filepath_not_found:
        raise FileNotFoundError(
            "The resource `{}` could not be found.".format(resource_name)
        )
    return potential_path


__all__ = [
    "CreatesCurves",
    "get_resource_path",
    "Static",
    "NonLinear0",
    "plot_curves",
    "make_family_overview_plots",
]

_SAMPLE_CURVE_ROOT_PATH = Path(__file__).parent.joinpath("curves")
_DEFAULT_ABSCISSA_NAME = "x"
_DEFAULT_COLUMN_LABELS = "abcdefghqrstvy"

BasePoints = List[Tuple[float, float]]
"""
*Base points* should not contain a large amount of x, y points compared to a 
curve.
"""

AnArray = Union[numpy.ndarray, Iterable[float]]
"""
In this context an iterable of floats is meant by an array.
"""


def _get_family_key(family_name: str) -> str:
    assert isinstance(family_name, str), "`family_name` must be a string."
    assert family_name != "", "`family_name` must not be empty."
    return family_name.lower()


def _split_first_column(curves: numpy.ndarray) -> Tuple[numpy.ndarray, numpy.ndarray]:
    """

    Args:
        curves:

    Returns:

    Examples:
        >>> import numpy
        >>> xy_curves = numpy.arange(12).reshape(4, 3)
        >>> xy_curves
        array([[ 0,  1,  2],
               [ 3,  4,  5],
               [ 6,  7,  8],
               [ 9, 10, 11]])
        >>> outer_left_column, remaining_columns = _split_first_column(xy_curves)
        >>> outer_left_column
        array([0, 3, 6, 9])
        >>> remaining_columns
        array([[ 1,  2],
               [ 4,  5],
               [ 7,  8],
               [10, 11]])

    """
    return curves[:, 0], curves[:, 1:]


def _calculate_curve_by_cubic_spline(
    base_points: BasePoints, target_x: AnArray
) -> DataFrame:
    """

    Args:
        base_points:
        target_x:

    Returns:
        numpy.ndarray

    Raises:
        ValueError:
            If base points shape exceeds (n, m).

    Examples:
        >>> from doctestprinter import doctest_print
        >>> sample_base_points = [(0, 0), (2, 3), (8, 9), (10, 10)]
        >>> requested_x_values = list(range(6))
        >>> sample_curve = _calculate_curve_by_cubic_spline(
        ...     base_points=sample_base_points, target_x=requested_x_values
        ... )
        >>> doctest_print(sample_curve)
                  y
        x
        0.0  0.0000
        1.0  1.5625
        2.0  3.0000
        3.0  4.3125
        4.0  5.5000
        5.0  6.5625

    """
    base_points = np.array(base_points, dtype=float)
    deeply_multidimensional_array = len(base_points.shape) > 2
    if deeply_multidimensional_array:
        raise ValueError(
            "Only (n, m) shaped arrays are supported. Got to many dimensions."
        )
    not_enough_values = len(base_points.shape) < 2
    if not_enough_values:
        raise ValueError(
            "Only (n, m) shaped arrays are supported. Got only 1-dimension."
        )
    independent_x, multiple_y = _split_first_column(base_points)
    requested_x = np.array(target_x)
    cubic_spline = CubicSpline(independent_x, multiple_y)
    spline_y_values = cubic_spline(requested_x)
    requested_curve = DataFrame(
        spline_y_values.astype(float), index=pandas.Index(requested_x.astype(float))
    )
    requested_curve.index.name = _DEFAULT_ABSCISSA_NAME
    requested_curve.columns = [_DEFAULT_COLUMN_LABELS[-1]]
    return requested_curve


def _offset_curves(
    curves: DataFrame, offsets: Optional[Union[float, Iterable[float]]] = None
) -> DataFrame:
    """

    Args:
        curves:
        offsets:

    Returns:

    .. doctest:

        # Suppression Justification; Private member imported only for testing.
        >>> # noinspection PyProtectedMember
        >>> from examplecurves.main import _offset_curves
        >>> from pandas import DataFrame
        >>> sample_frame = DataFrame([[1, 2, 3]], index=[0], columns=list(iter("abc")))
        >>> from doctestprinter import doctest_print
        >>> doctest_print(_offset_curves(sample_frame))
           a  b  c
        0  1  2  3
        >>> doctest_print(_offset_curves(sample_frame, 0.1))
             a  b  c
        0.1  1  2  3
        >>> doctest_print(_offset_curves(sample_frame, [0.1, 0.2, 0.3]))
               a    b  c
        0.1  1.2  2.3  3
        >>> doctest_print(_offset_curves(sample_frame, [0.1, 0.2, 0.3, 0.4, 0.5]))
               a    b    c
        0.1  1.2  2.3  3.4
    """
    if offsets is None:
        return curves

    if not isinstance(offsets, (list, tuple)):
        offsets = [offsets]

    x_offset, *y_offsets = offsets
    requested_curves = curves.copy()
    requested_curves.index += x_offset
    curve_count = len(requested_curves.columns)
    for index, y_offset in enumerate(y_offsets[:curve_count]):
        active_columns = requested_curves.columns[index]
        requested_curves[active_columns] += y_offset

    return requested_curves


@overload
def _offset_curves_in_place(
    curves: List[DataFrame], offsets: Optional[Sequence[float]] = None
):
    pass  # pragma: no cover


@overload
def _offset_curves_in_place(
    curves: List[DataFrame], offsets: Optional[Sequence[Sequence[float]]] = None
):
    pass  # pragma: no cover


def _offset_curves_in_place(
    curves: List[DataFrame],
    offsets: Optional[Union[Sequence[float], Sequence[Sequence[float]]]] = None,
):
    """
    Args:
        curves:
        offsets:

    .. doctest:

        # Suppression Justification; Private member imported only for testing.
        >>> # noinspection PyProtectedMember
        >>> from examplecurves.main import _offset_curves_in_place
        >>> from pandas import DataFrame, Index
        >>> from doctestprinter import doctest_print
        >>> test_frame = DataFrame([0], columns=["y"], index=Index([0], name="x"))
        >>> sample_curves = [test_frame.copy(), test_frame.copy()]
        >>> _offset_curves_in_place(curves=sample_curves, offsets=[1.0])
        Traceback (most recent call last):
            ...
        ValueError: There must be 2 curve offsets defined. Got only 1.
        >>> _offset_curves_in_place(curves=sample_curves, offsets=[1.0, 2.0])
        >>> for item in sample_curves:
        ...     doctest_print(item)
             y
        x
        1.0  0
             y
        x
        2.0  0
        >>> sample_curves = [test_frame.copy(), test_frame.copy()]
        >>> _offset_curves_in_place(
        ...     curves=sample_curves, offsets=[(1.0, 1.0), (2.0, 2.0)]
        ... )
        >>> for item in sample_curves:
        ...     doctest_print(item)
               y
        x
        1.0  1.0
               y
        x
        2.0  2.0
    """
    no_offsets_defined_so_do_nothing = offsets is None
    if no_offsets_defined_so_do_nothing:
        return None

    count_of_sample_curves = len(curves)
    offset_count = len(offsets)
    if offset_count < count_of_sample_curves:
        raise ValueError(
            "There must be {} curve offsets defined. Got only {}."
            "".format(count_of_sample_curves, offset_count)
        )

    for index in range(len(curves)):
        curves[index] = _offset_curves(curves=curves[index], offsets=offsets[index])


_GROUP10_SPLINE_ARGS = numpy.array(
    list(zip([0.0, 0.2, 0.8, 1.0], [0.0, 0.3, 0.9, 1.0]))
)
_GROUP10_TARGET_X = numpy.arange(0.0, 1.1, 0.1)


CurveCreationParameters = namedtuple(
    "CurveCreationParameters", "creation_function curve_key_arguments offsets"
)


class CreatesCurves(ABC):
    @staticmethod
    @abstractmethod
    # no coverage of abstract methods
    def make(**kwargs) -> Series:  # pragma: no cover
        """
        This method *makes* a curve based on a set of parameters.

        Args:
            **kwargs:
                Curve creation keyword arguments.

        Returns:
            Series
        """
        pass
        raise NotImplementedError(
            "This method needs to implement "
            "the creation of a curve sample upon keyword arguments."
        )

    @classmethod
    @abstractmethod
    # no coverage of abstract methods
    def get_curve_creation_parameters(cls) -> List[Dict]:  # pragma: no cover
        """
        Returns parameters to create a specific curve.

        Returns:
            List[Dict]
        """
        pass

    @classmethod
    def iter_curve_creation_parameters(
        cls, selection_indexes: Optional[List[int]] = None
    ) -> Generator[Dict, None, None]:
        all_parameters = cls.get_curve_creation_parameters()
        if selection_indexes is not None:
            selected_creation_parameters = [
                copy.deepcopy(parameters)
                for index, parameters in enumerate(all_parameters)
                if index in selection_indexes
            ]
        else:
            selected_creation_parameters = copy.deepcopy(all_parameters)
        return selected_creation_parameters

    @classmethod
    @abstractmethod
    # no coverage of abstract methods
    def get_offsets(cls, offset_index: int):  # pragma: no cover
        """
        Returns a predefined offset.

        Args:
            offset_index(int):
                The index of the offset, which should be returned. Is equal
                to the index of the curve.

        Returns:

        """
        pass

    @classmethod
    @abstractmethod
    # no coverage of abstract methods
    def get_offset_count(cls) -> int:  # pragma: no cover
        """
        Returns the count of predefined offsets.

        Returns:
            int
        """
        pass


class NonLinear0(CreatesCurves):
    """
    5 non linear curves with a light curvature. Each curve has 11 points.

    Examples:
        >>> import examplecurves
        >>> non_linear_curves_no_0 = examplecurves.Static.create("nonlinear0")
        >>> from doctestprinter import doctest_print
        >>> doctest_print(non_linear_curves_no_0[1])
                   y
        x
        0.0   0.0000
        0.1   1.5625
        0.2   3.0000
        0.3   4.3125
        0.4   5.5000
        0.5   6.5625
        0.6   7.5000
        0.7   8.3125
        0.8   9.0000
        0.9   9.5625
        1.0  10.0000

    .. doctest::

        >>> from examplecurves import NonLinear0
        >>> NonLinear0.get_offset_count()
        2

    .. plot::

        from examplecurves import make_family_overview_plots
        make_family_overview_plots("nonlinear0")

    """

    SPLINE_ARGS = numpy.array([(0.0, 0.0), (0.2, 0.3), (0.8, 0.9), (1.0, 1.0)])
    TARGET_X = numpy.arange(0.0, 1.1, 0.1)

    CURVE_CREATION_PARAMETERS = [
        {
            "base_points": SPLINE_ARGS * [1.15, 9.0],
            "target_x": TARGET_X * 1.15,
        },
        {
            "base_points": SPLINE_ARGS * [1.0, 10.0],
            "target_x": TARGET_X,
        },
        {
            "base_points": SPLINE_ARGS * [1.1, 10.2],
            "target_x": TARGET_X * 1.11,
        },
        {
            "base_points": SPLINE_ARGS * [0.96, 11.5],
            "target_x": TARGET_X * 0.96,
        },
        {
            "base_points": SPLINE_ARGS * [0.9, 11.5],
            "target_x": TARGET_X * 0.9,
        },
    ]

    OFFSETS = [
        [0.08, 0.1, 0.05, 0.01, 0.02],
        [(0.08, 0.01), (0.1, 0.05), (0.05, 0.1), (0.01, 0.08), (0.02, 0.0)],
    ]

    def __new__(cls, *args, **kwargs):
        return cls

    @staticmethod
    def make(**kwargs):
        return _calculate_curve_by_cubic_spline(**kwargs)

    @classmethod
    def get_curve_creation_parameters(cls) -> List[Dict]:
        return cls.CURVE_CREATION_PARAMETERS

    @classmethod
    def get_offsets(cls, offset_index: int):
        return copy.deepcopy(cls.OFFSETS[offset_index])

    @classmethod
    def get_offset_count(cls):
        return len(cls.OFFSETS)


def _create_linear_curve(end_point: numpy.ndarray, curve_length: int = 5) -> DataFrame:
    """
    Creates a linear curve from origin to the requested *end point*.

    Args:
        end_point(numpy.ndarray):
            A simple 2-dimensional point, which marks the curves end.

        curve_length(int):
            Number of values the resulting curve has.

    Returns:
        DataFrame

    .. doctest::

        >>> from doctestprinter import doctest_print
        >>> doctest_print(_create_linear_curve(numpy.array([1.0, 10.0])))
                 y
        x
        0.00   0.0
        0.25   2.5
        0.50   5.0
        0.75   7.5
        1.00  10.0
        >>> _create_linear_curve(numpy.array([1.0, 10.0]), curve_length=1)
        Traceback (most recent call last):
        ...
        ValueError: The curve cannot have less than 2 points.

    """
    if curve_length < 2:
        raise ValueError("The curve cannot have less than 2 points.")
    x, y = end_point
    x_values = np.linspace(0.0, x, num=curve_length)
    y_values = np.linspace(0.0, y, num=curve_length)
    requested_frames = DataFrame(
        y_values, columns=["y"], index=pandas.Index(x_values, name="x")
    )
    return requested_frames


class LoadsLinearCurves(CreatesCurves):
    CREATION_PARAMETERS_ADDRESS_PART = "curve_creation_parameters"
    OFFSET_ADDRESS_PART = "offsets"
    RESOURCE_FILENAME = "linear_curves.json"

    def __init__(self, family_name: Optional[str] = None, *args, **kwargs):
        """
        .. doctest:

            >>> test_loader = LoadsLinearCurves()
            >>> test_loader.get_offset_count()
            0
            >>> test_loader.get_curve_creation_parameters()
            [{'end_point': [1.0, 10.0], 'curve_length': 3}]
            >>> from doctestprinter import doctest_iter_print
            >>> doctest_iter_print(test_loader.iter_curve_creation_parameters())
            {'end_point': [1.0, 10.0], 'curve_length': 3}

        """
        if family_name is None:
            self._family_name = self.__class__.__name__
        else:
            self._family_name = family_name
        self._creation_parameters = []
        self._offsets = []

        family_key_name = _get_family_key(self._family_name)

        parameters_and_offsets = self.read_parameters(family_key_name)
        parameters_key = self.CREATION_PARAMETERS_ADDRESS_PART
        if self.CREATION_PARAMETERS_ADDRESS_PART in parameters_and_offsets:
            self._creation_parameters = parameters_and_offsets[parameters_key]

        offsets_key = self.OFFSET_ADDRESS_PART
        if self.OFFSET_ADDRESS_PART in parameters_and_offsets:
            self._creation_parameters = parameters_and_offsets[offsets_key]

    def __repr__(self):
        return "{}({})".format(self.__class__.__name__, self._family_name)

    def iter_curve_creation_parameters(
        self, selection_indexes: Optional[List[int]] = None
    ) -> Generator[Dict, None, None]:
        all_parameters = self.get_curve_creation_parameters()
        if selection_indexes is not None:
            selected_creation_parameters = [
                copy.deepcopy(parameters)
                for index, parameters in enumerate(all_parameters)
                if index in selection_indexes
            ]
        else:
            selected_creation_parameters = copy.deepcopy(all_parameters)
        return selected_creation_parameters

    @classmethod
    def register_creation_parameters(
        cls, family_name: str, curve_creation_parameters: List[dict]
    ):
        """
        Registers creation parameters of a *family name* in the resources file.

        Args:
            family_name(str):
                The family name of the targeted curves.

            curve_creation_parameters(List[dict]):
                The creation keyword arguments for each curve.

        """
        family_key_name = _get_family_key(family_name=family_name)
        resource_filepath = get_resource_path(cls.RESOURCE_FILENAME)
        parameter_address = (
            family_key_name + ADDRESS_DELIMITER + cls.CREATION_PARAMETERS_ADDRESS_PART
        )
        put_into_json_file(
            filepath=resource_filepath,
            data=curve_creation_parameters,
            address=parameter_address,
        )

    @classmethod
    def register_offsets(cls, family_name: str, offsets):
        """
        Registers offsets of a *family name* in the resources file.

        Args:
            family_name(str):
                The family name of the targeted curves.

            offsets:
                The offsets for the targeted curves.

        """
        family_key_name = _get_family_key(family_name=family_name)
        resource_filepath = get_resource_path(cls.RESOURCE_FILENAME)
        offset_address = family_key_name + ADDRESS_DELIMITER + cls.OFFSET_ADDRESS_PART
        put_into_json_file(
            filepath=resource_filepath, data=offsets, address=offset_address
        )

    @classmethod
    def read_parameters(cls, family_name: str) -> dict:
        """

        Args:
            family_name:

        Returns:
            dict:
                A dictionary with *cls.CREATION_PARAMETERS_ADDRESS_PART* and
                *cls.OFFSET_ADDRESS_PART*.

        .. doctest:

            >>> creates_curves = LoadsLinearCurves()
            >>> from doctestprinter import doctest_iter_print
            >>> creation_pars = creates_curves.read_parameters("HorizontalLinear0")
            >>> doctest_iter_print(creation_pars["curve_creation_parameters"])
            {'end_point': [1.022278673972714, 10.018633045765489], 'curve_length': 5}
            {'end_point': [1.0202814839730938, 10.01560397208917], 'curve_length': 5}
            {'end_point': [1.0155758653529496, 10.003419925231901], 'curve_length': 5}
            {'end_point': [1.0280393839395214, 10.043892394771133], 'curve_length': 5}
            {'end_point': [0.9693177328392936, 9.998681845454435], 'curve_length': 5}

        """
        resource_filepath = get_resource_path(cls.RESOURCE_FILENAME)
        family_key_name = _get_family_key(family_name=family_name)
        parameter_and_offsets = read_from_json_file(
            filepath=resource_filepath, address=family_key_name
        )
        return parameter_and_offsets

    @staticmethod
    def make(**kwargs):
        return _create_linear_curve(**kwargs)

    def get_curve_creation_parameters(self) -> List[Dict]:
        return copy.deepcopy(self._creation_parameters)

    def get_offsets(self, offset_index: int):
        try:
            return copy.deepcopy(self._offsets[offset_index])
        except IndexError:
            if offset_index == 0:
                raise IndexError("The family of curves has no offsets defined.")
            raise IndexError(
                "The requested index is out of bound of the available offsets."
            )

    def get_offset_count(self):
        return len(self._offsets)


SAMPLE_CURVE_CREATORS = {
    "nonlinear0": NonLinear0,
    "horizontallinear0": LoadsLinearCurves,
    "horizontallinear1": LoadsLinearCurves,
    "horizontallinear2": LoadsLinearCurves,
    "horizontallinear3": LoadsLinearCurves,
    "diagonallinear0": LoadsLinearCurves,
    "diagonallinear1": LoadsLinearCurves,
    "diagonallinear2": LoadsLinearCurves,
    "diagonallinear3": LoadsLinearCurves,
    "verticallinear0": LoadsLinearCurves,
    "verticallinear1": LoadsLinearCurves,
    "verticallinear2": LoadsLinearCurves,
    "verticallinear3": LoadsLinearCurves,
}


@overload
def _cut_curves_in_place(curves: List[DataFrame], cut_curves_at: int):
    pass  # pragma: no cover


@overload
def _cut_curves_in_place(curves: List[DataFrame], cut_curves_at: List[int]):
    pass  # pragma: no cover


def _cut_curves_in_place(curves: List[DataFrame], cut_curves_at: Union[int, List[int]]):
    """

    Args:
        curves:

    Returns:

    .. doctest:

        # Suppression Justification; Private member imported only for testing.
        >>> # noinspection PyProtectedMember
        >>> from examplecurves.main import _cut_curves_in_place
        >>> import numpy
        >>> sample_curves = [DataFrame(numpy.arange(5))]
        >>> sample_curves[0]
           0
        0  0
        1  1
        2  2
        3  3
        4  4
        >>> _cut_curves_in_place(sample_curves, 2)
        >>> sample_curves[0]
           0
        0  0
        1  1
        >>> sample_curves = [DataFrame(numpy.arange(5))]
        >>> _cut_curves_in_place(sample_curves, [2, 4])
        >>> sample_curves[0]
           0
        2  2
        3  3
        >>> sample_curves = [DataFrame(numpy.arange(5))]
        >>> _cut_curves_in_place(sample_curves, [-4, None, 2])
        >>> sample_curves[0]
           0
        1  1
        3  3
    """
    if isinstance(cut_curves_at, (list, tuple)):
        curve_value_selection_slice = slice(*cut_curves_at)
    else:
        curve_value_selection_slice = slice(cut_curves_at)

    for index, curve_filepath in enumerate(curves):
        curves[index] = curves[index].iloc[curve_value_selection_slice]


def _get_curve_creator(family_name: str) -> CreatesCurves:
    """
    Retrieves the instance/class which creates curves.

    Args:
        family_name(str):
            The name of the requested family of curves.

    Returns:
        CreatesCurves

    .. doctest:

        >>> _get_curve_creator("test_family")
        Traceback (most recent call last):
        ...
        KeyError: 'No curves with the family name `test_family` are registered.'
        >>> _get_curve_creator("NoNlINear0")
        <class 'examplecurves.main.NonLinear0'>

    """
    assert (
        family_name is not None
    ), "`_get_curve_creator()` only permits non empty-strings."
    assert family_name != "", "`get_curve_creator()` only permits non empty-strings."
    family_key_name = _get_family_key(family_name=family_name)
    try:
        return SAMPLE_CURVE_CREATORS[family_key_name]
    except KeyError:
        raise KeyError(
            "No curves with the family name `{}` are registered.".format(family_name)
        )


class Static(object):
    @staticmethod
    def create(
        family_name: str,
        cut_curves_at: Optional[Union[int, List[int]]] = None,
        offsets: Optional[Union[Iterable[float], Iterable[Tuple[float, float]]]] = None,
        predefined_offset: Optional[int] = None,
        curve_selection: Optional[List[int]] = None,
    ) -> List[DataFrame]:
        """
        Creates static families of curves requested by name.

        Args:
            family_name:
                Name of the *family of curves*.

            cut_curves_at(Optional[Union[int, List[Optional[int]]]]):
                Cuts the curves at an integer position, os slices it by 2 or 3
                entries, where 'None' is a blank. Like [None, -3] being [:-3].

            offsets(Optional[Union[Iterable[float], Iterable[Tuple[float, float]]]]):
                Offsets to apply to the group's curves. Provide either abzissa offsets
                as a 1-dimensial array or absizza and ordinate offsets as a 2-dimensional
                array.

            predefined_offset(Optional[int]):
                Index of the group's predefined offsets to use. Overrules *offsets*.

            curve_selection(Optional[List[int]]):
                Number (0 .. n-1) of the curves, which should be actually be created.

        Returns:
            List[DataFrame]

        Examples:
            >>> import examplecurves
            >>> from doctestprinter import doctest_iter_print, doctest_print
            >>> sample_curves = examplecurves.Static.create(
            ...     family_name="nonlinear0", cut_curves_at=[2, 8, 2]
            ... )
            >>> doctest_iter_print(sample_curves)
                     y
            x
            0.23  2.70
            0.46  4.95
            0.69  6.75
                   y
            x
            0.2  3.0
            0.4  5.5
            0.6  7.5
                          y
            x
            0.222  3.085479
            0.444  5.651643
            0.666  7.698492
                       y
            x
            0.192  3.450
            0.384  6.325
            0.576  8.625
                      y
            x
            0.18  3.450
            0.36  6.325
            0.54  8.625
            >>> sample_curves = examplecurves.Static.create(
            ...     family_name="nonlinear0",
            ...     cut_curves_at=[2, 4],
            ...     predefined_offset=1,
            ...     curve_selection=[1]
            ... )
            >>> doctest_print(sample_curves[0])
                       y
            x
            0.28  3.0100
            0.38  4.3225

        """
        family_key_name = _get_family_key(family_name=family_name)
        if family_key_name not in SAMPLE_CURVE_CREATORS:
            raise ValueError(
                "Example curve group '{}' could not be found.".format(family_name)
            )
        creates_curves = SAMPLE_CURVE_CREATORS[family_key_name](family_name=family_name)

        if predefined_offset is not None:
            try:
                offsets = creates_curves.get_offsets(predefined_offset)
            except IndexError:
                raise IndexError(
                    "The group '{}' doesn't have offsets defined at the index '{}'"
                    "".format(offsets)
                )

        requested_curves = []
        for (
            creation_keyword_parameters
        ) in creates_curves.iter_curve_creation_parameters(
            selection_indexes=curve_selection
        ):
            created_curves = creates_curves.make(**creation_keyword_parameters)
            requested_curves.append(created_curves)

        count_of_sample_curves = len(requested_curves)
        if count_of_sample_curves == 0:
            raise ValueError(
                "No sample curves for of the group-index '{}' "
                "where found in '{}'".format(family_name, _SAMPLE_CURVE_ROOT_PATH)
            )

        _cut_curves_in_place(curves=requested_curves, cut_curves_at=cut_curves_at)
        _offset_curves_in_place(curves=requested_curves, offsets=offsets)
        return requested_curves


# This function is not covered, because matplotlib ***** up testing in tox,
# while pytest runs smoothly. Testing is either done manually and
# by checking the documentation, which makes use of these methods.
def _plot_curves(
        curves: List[DataFrame], title: Optional[str] = None
):
    import matplotlib.pyplot as plt
    fig = plt.figure(figsize=(8, 5), dpi=96, tight_layout=True)
    gs = fig.add_gridspec(1, 10)
    axes = fig.add_subplot(gs[:, :9])
    if title:
        axes.set_title(title)
    for index, curve in enumerate(curves):
        axes.plot(curve, "-o", label=str(index))
    fig.legend(loc="upper right", bbox_to_anchor=(0.99, 0.945))
    return fig


# This function is not covered, because matplotlib ***** up testing in tox,
# while pytest runs smoothly. Testing is either done manually and
# by checking the documentation, which makes use of these methods.
def plot_curves(
        curves: List[DataFrame], title: Optional[str] = None
):
    """
    Plots curves within a diagram.

    Args:
        curves(List[DataFrame]):
            Curves to plot.

        title(Optional[str]):
            Optional title for the diagram.

    """
    import matplotlib.pyplot as plt
    fig = _plot_curves(curves=curves, title=title)
    fig.show()
    plt.close(fig)


# This function is not covered, because matplotlib ***** up testing in tox,
# while pytest runs smoothly. Testing is either done manually and
# by checking the documentation, which makes use of these methods.
def _make_family_overview_plots(family_name: str):
    """
    Plots each predefined offset example of the *family of curves*.

    Args:
        family_name(str):
            Name of the exemplary family of curves.

    """
    import matplotlib.pyplot as plt
    creates_curves = _get_curve_creator(family_name=family_name)()
    number_of_offsets = creates_curves.get_offset_count()

    example_title = "{}'s curves".format(family_name)
    curves = Static.create(family_name=family_name)
    plot_figures = []
    fig = _plot_curves(curves, title=example_title)
    plot_figures.append(fig)

    for offset_index in range(number_of_offsets):
        example_title = "{}'s curves with offsets at index {}".format(
            family_name, offset_index
        )
        curves = Static.create(family_name=family_name, predefined_offset=offset_index)
        fig = _plot_curves(curves, title=example_title)
        plot_figures.append(fig)

    return plot_figures


# This function is not covered, because matplotlib ***** up testing in tox,
# while pytest runs smoothly. Testing is either done manually and
# by checking the documentation, which makes use of these methods.
def make_family_overview_plots(family_name: str):
    """
    Plots each predefined offset example of the *family of curves*.

    Args:
        family_name(str):
            Name of the exemplary family of curves.

    """
    import matplotlib.pyplot as plt
    plot_figures = _make_family_overview_plots(family_name=family_name)
    for fig in plot_figures:
        fig.show()

    for fig in plot_figures:
        plt.close(fig)