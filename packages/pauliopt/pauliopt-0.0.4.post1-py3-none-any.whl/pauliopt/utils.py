"""
    Utility classes and functions for the `pauliopt` library.
"""

import math
from decimal import Decimal
from fractions import Fraction
from typing import (Final, List, Literal, Mapping, Optional, overload,
                    Protocol, runtime_checkable, Sequence, Tuple, Union)

AngleInitT = Union[int, Fraction, Decimal, str]

class Angle:
    """
        A container class for angles,
        as rational multiples of PI modulo 2PI.

        Copyright (C) 2019 - Hashberg Ltd
    """

    _value: Fraction

    def __init__(self, theta: Union["Angle", AngleInitT]):
        if isinstance(theta, Angle):
            self._value = theta.value
        else:
            self._value = Fraction(theta)

    @property
    def value(self) -> Fraction:
        """
            The value of this angle as a fraction of PI.
        """
        return self._value%2

    @property
    def as_root_of_unity(self) -> Tuple[int, int]:
        """
            Returns `(a,n)` where `n` is the smallest such
            that this angle is an $n$-th root of unity
            and `0 <= a < n` such that this is $e^{i 2\\pi \\frac{a}{n}}$
        """
        num = self.value.numerator
        den = self.value.denominator
        a: int = num//2 if num%2 == 0 else num
        order: int = den if num % 2 == 0 else 2*den
        return (a, order)

    @property
    def order(self):
        """
            The order of this angle as a root of unity.
        """
        num = self.value.numerator
        den = self.value.denominator
        return den if num % 2 == 0 else 2*den

    @property
    def is_zero_or_pi(self) -> bool:
        """
            Whether this angle is a multiple of pi.
        """
        num = self.value.numerator
        den = self.value.denominator
        return num % den == 0

    @property
    def is_zero(self) -> bool:
        """
            Whether this angle is a multiple of 2pi.
        """
        num = self.value.numerator
        den = self.value.denominator
        return num % (2*den) == 0

    @property
    def is_pi(self) -> bool:
        """
            Whether this angle is an odd multiple of pi.
        """
        num = self.value.numerator
        den = self.value.denominator
        return num % den == 0 and not num % (2*den) == 0

    def __pos__(self) -> "Angle":
        return self

    def __neg__(self) -> "Angle":
        return Angle(-self._value)

    def __add__(self, other: "Angle") -> "Angle":
        if isinstance(other, Angle):
            return Angle(self._value + other._value)
        return NotImplemented

    def __sub__(self, other: "Angle") -> "Angle":
        if isinstance(other, Angle):
            return Angle(self._value - other._value)
        return NotImplemented

    def __mod__(self, other: "Angle") -> "Angle":
        if isinstance(other, Angle):
            return Angle(self._value % other._value)
        return NotImplemented

    def __mul__(self, other: Union[int, Fraction, str]) -> "Angle":
        if isinstance(other, int):
            return Angle(self._value * Fraction(other))
        return NotImplemented

    def __rmul__(self, other: Union[int, Fraction, str]) -> "Angle":
        if isinstance(other, int):
            return Angle(self._value * Fraction(other))
        return NotImplemented

    def __truediv__(self, other: Union[int, Fraction, str]) -> "Angle":
        if isinstance(other, int):
            return Angle(self._value / Fraction(other))
        return NotImplemented

    def __hash__(self) -> int:
        return hash(repr(self))

    def __str__(self) -> str:
        num = self.value.numerator
        den = self.value.denominator
        if num == 0:
            return "0"
        if num == 1:
            if den == 1:
                return "π"
            return "π/%d"%den
        return "%dπ/%d"%(num, den)

    def __repr__(self) -> str:
        num = self.value.numerator
        den = self.value.denominator
        if num == 0:
            return "Angle.zero"
        if num == 1:
            if den == 1:
                return "Angle.pi"
            return "Angle.pi/%d"%den
        return "%d*Angle.pi/%d"%(num, den)

    @property
    def repr_latex(self) -> str:
        """
            LaTeX math mode representation of this number.
        """
        num = self.value.numerator
        den = self.value.denominator
        if num == 0:
            return "0"
        if num == 1:
            if den == 1:
                return "\\pi"
            return "\\frac{\\pi}{%d}"%den
        return "\\frac{%d\\pi}{%d}"%(num, den)

    def _repr_latex_(self):
        """
            Magic method for IPython/Jupyter pretty-printing.
            See https://ipython.readthedocs.io/en/stable/api/generated/IPython.display.html
        """
        return "$%s$"%self.repr_latex

    def __eq__(self, other):
        if other == 0:
            return self.value == 0
        if not isinstance(other, Angle):
            return NotImplemented
        return self.value == other.value

    def __float__(self) -> float:
        return float(self.value)*math.pi

    @overload
    @staticmethod
    def random(subdivision: int = 4, *,
               size: Literal[1]=1,
               rng_seed: Optional[int] = None) -> "Angle":
        ...

    @overload
    @staticmethod
    def random(subdivision: int = 4, *,
               size: int = 1,
               rng_seed: Optional[int] = None) -> Union["Angle", Tuple["Angle", ...]]:
        ...

    @staticmethod
    def random(subdivision: int = 4, *, size: int = 1, rng_seed: Optional[int] = None):
        """
            Generates a random angle with the given `subdivision`:
            `r * pi/subdivision` for random `r in range(2*subdivision)`.

            Requires `numpy`.
        """
        if not isinstance(subdivision, int):
            raise TypeError()
        if not isinstance(size, int):
            raise TypeError()
        if subdivision <= 0:
            raise ValueError("Subdivision must be positive.")
        if size <= 0:
            raise ValueError("Size must be positive.")
        if rng_seed is not None and not isinstance(rng_seed, int):
            raise TypeError("RNG seed must be integer or 'None'.")
        try:
            # pylint: disable = import-outside-toplevel, unused-import
            import numpy as np # type: ignore
        except ModuleNotFoundError as _:
            raise ModuleNotFoundError("You must install the 'numpy' library.")
        rng = np.random.default_rng(seed=rng_seed)
        rs = rng.integers(2*subdivision, size=size)
        if size == 1:
            return Angle(Fraction(int(rs[0]), subdivision))
        return tuple(Angle(Fraction(int(r), subdivision)) for r in rs)

    zero: Final["Angle"] # type: ignore
    """ A constant for the angle 0. """

    pi: Final["Angle"] # type: ignore
    """ A constant for the angle pi. """

# Set static constants for Angle:
Angle.zero = Angle(0) # type: ignore
Angle.pi = Angle(1) # type: ignore


pi: Final[Angle] = Angle.pi
""" Constant for `Angle.pi`. """

π: Final[Angle] = Angle.pi
""" Constant for `Angle.pi`. """


def _validate_vec2(vec2: Tuple[int, int]):
    if not isinstance(vec2, tuple) or len(vec2) != 2:
        raise TypeError("Expected pair.")
    if not all(isinstance(x, int) for x in vec2):
        raise TypeError("Expected pair of integers.")

class SVGBuilder:
    """
        Utility class for building certain SVG images.
        Follows the [Fluent interface pattern](https://en.wikipedia.org/wiki/Fluent_interface).
    """

    _width: int
    _height: int
    _tags: List[str]

    def __init__(self, width: int, height: int):
        if not isinstance(width, int) or width <= 0:
            raise TypeError("Width should be positive integer.")
        if not isinstance(height, int) or height <= 0:
            raise TypeError("Height should be positive integer.")
        self._width = width
        self._height = height
        self._tags = []

    @property
    def width(self) -> int:
        """
            The figure width.
        """
        return self._width

    @width.setter
    def width(self, new_width: int):
        """
            Set the figure width.
        """
        if not isinstance(new_width, int) or new_width <= 0:
            raise TypeError("Width should be positive integer.")
        self._width = new_width

    @property
    def height(self) -> int:
        """
            The figure height.
        """
        return self._height

    @height.setter
    def height(self, new_height: int):
        """
            Set the figure height.
        """
        if not isinstance(new_height, int) or new_height <= 0:
            raise TypeError("Height should be positive integer.")
        self._height = new_height

    @property
    def tags(self) -> Sequence[str]:
        """
            The current sequence of tags.
        """
        return self._tags

    def line(self, fro: Tuple[int, int], to: Tuple[int, int]) -> "SVGBuilder":
        """
            Draws a line from given coordinates to given coordinates.
        """
        _validate_vec2(fro)
        _validate_vec2(to)
        fx, fy = fro
        tx, ty = to
        tag = (f'<path fill="none" stroke="black"'
               f' d="M {fx}, {fy} L {tx}, {ty}"/>')
        self._tags.append(tag)
        return self

    def circle(self, centre: Tuple[int, int], r: int, fill: str) -> "SVGBuilder":
        """
            Draws a circle with given centre and radius.
        """
        _validate_vec2(centre)
        if not isinstance(fill, str):
            raise TypeError("Fill must be string.")
        x, y = centre
        tag = (f'<circle fill="{fill}" stroke="black"'
               f' cx="{x}" cy="{y}" r="{r}"/>')
        self._tags.append(tag)
        return self

    def text(self, pos: Tuple[int, int], text: str, *, font_size: int = 10) -> "SVGBuilder":
        """
            Draws text at the given position (stroke/fill not used).
        """
        _validate_vec2(pos)
        if not isinstance(text, str):
            raise TypeError("Text must be string.")
        if not isinstance(font_size, int) or font_size <= 0:
            raise TypeError("Font size must be positive integer.")
        x, y = pos
        tag = f'<text x="{x}" y="{y+font_size//4}" font-size="{font_size}">{text}</text>'
        self._tags.append(tag)
        return self

    def __repr__(self) -> str:
        # pylint: disable = line-too-long
        body = "\n".join(self._tags)
        headers = "\n".join([
            '<?xml version="1.0" encoding="utf-8"?>',
            '<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">',
        ])
        return f'{headers}\n<svg version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{self.width}" height="{self.height}">{body}\n</svg>'

    def __irshift__(self, other: "SVGBuilder") -> "SVGBuilder":
        if not isinstance(other, SVGBuilder):
            raise TypeError(f"Expected SVGBuilder, found {type(other)}")
        for tag in other._tags:
            self._tags.append(tag)
        return self


@runtime_checkable
class TempSchedule(Protocol):
    """
        Protocol for a temperature schedule.
        The temperature is a number (int or float) computed from the iteration
        number `it` (starting from 0) and the total number of iterations `num_iter`
        (passed as a keyword argument).
    """

    def __call__(self, it: int, num_iters: int) -> float:
        ...

@runtime_checkable
class TempScheduleProvider(Protocol):
    """
        Protocol for a function constructing a temperature schedule
        from an initial and final temperatures.
    """

    def __call__(self, t_init: Union[int, float], t_final: Union[int, float]) -> TempSchedule:
        ...


def linear_temp_schedule(t_init: Union[int, float], t_final: Union[int, float]) -> TempSchedule:
    """
        Returns a straight/linear temperature schedule for given initial and final temperatures,
        from https://link.springer.com/article/10.1007/BF00143921
    """
    if not isinstance(t_init, (int, float)):
        raise TypeError(f"Expected int or float, found {type(t_init)}.")
    if not isinstance(t_final, (int, float)):
        raise TypeError(f"Expected int or float, found {type(t_final)}.")
    def temp_schedule(it: int, num_iters: int) -> float:
        return t_init + (t_final-t_init)*it/(num_iters-1)
    return temp_schedule


def geometric_temp_schedule(t_init: Union[int, float], t_final: Union[int, float]) -> TempSchedule:
    """
        Returns a geometric temperature schedule for given initial and final temperatures,
        from https://link.springer.com/article/10.1007/BF00143921
    """
    if not isinstance(t_init, (int, float)):
        raise TypeError(f"Expected int or float, found {type(t_init)}.")
    if not isinstance(t_final, (int, float)):
        raise TypeError(f"Expected int or float, found {type(t_final)}.")
    def temp_schedule(it: int, num_iters: int) -> float:
        return t_init * ((t_final/t_init)**(it/(num_iters-1)))
    return temp_schedule


def reciprocal_temp_schedule(t_init: Union[int, float], t_final: Union[int, float]) -> TempSchedule:
    """
        Returns a reciprocal temperature schedule for given initial and final temperatures,
        from https://link.springer.com/article/10.1007/BF00143921
    """
    if not isinstance(t_init, (int, float)):
        raise TypeError(f"Expected int or float, found {type(t_init)}.")
    if not isinstance(t_final, (int, float)):
        raise TypeError(f"Expected int or float, found {type(t_final)}.")
    def temp_schedule(it: int, num_iters: int) -> float:
        num = t_init*t_final*(num_iters-1)
        denom = (t_final*num_iters-t_init)+(t_init-t_final)*(it+1)
        return num/denom
    return temp_schedule


def log_temp_schedule(t_init: Union[int, float], t_final: Union[int, float]) -> TempSchedule:
    """
        Returns a logarithmic temperature schedule for given initial and final temperatures,
        from https://link.springer.com/article/10.1007/BF00143921
    """
    if not isinstance(t_init, (int, float)):
        raise TypeError(f"Expected int or float, found {type(t_init)}.")
    if not isinstance(t_final, (int, float)):
        raise TypeError(f"Expected int or float, found {type(t_final)}.")
    def temp_schedule(it: int, num_iters: int) -> float:
        num = t_init*t_final*(math.log(num_iters+1)-math.log(2))
        denom = (t_final*math.log(num_iters+1)-t_init*math.log(2))+(t_init-t_final)*math.log(it+2)
        return num/denom
    return temp_schedule


StandardTempScheduleName = Literal["linear", "geometric", "reciprocal", "log"]
"""
    Names of the standard temperature schedules.
"""


StandardTempSchedule = Tuple[StandardTempScheduleName,
                             Union[int, float], Union[int, float]]
"""
    Type for standard temperature schedules.
"""


StandardTempSchedules: Final[Mapping[StandardTempScheduleName, TempScheduleProvider]] = {
    "linear": linear_temp_schedule,
    "geometric": geometric_temp_schedule,
    "reciprocal": reciprocal_temp_schedule,
    "log": log_temp_schedule,
}
"""
    Dictionary of standard temperature schedule providers.
"""
