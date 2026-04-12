# -*- coding: utf-8 -*-
"""
GrayPaintScale - A paint scale that returns shades of gray.
"""

from typing import Tuple
import copy


class PaintScale:
    """Interface for paint scales."""
    
    def get_lower_bound(self) -> float:
        raise NotImplementedError
    
    def get_upper_bound(self) -> float:
        raise NotImplementedError
    
    def get_paint(self, value: float) -> Tuple[int, int, int]:
        raise NotImplementedError


class GrayPaintScale(PaintScale):
    """
    A paint scale that returns shades of gray.
    
    This is a complete translation of JFreeChart's GrayPaintScale class.
    """
    
    def __init__(self, lower_bound: float = 0.0, upper_bound: float = 1.0):
        """
        Creates a new GrayPaintScale instance.
        
        Args:
            lower_bound: the lower bound
            upper_bound: the upper bound
            
        Raises:
            ValueError: if lower_bound >= upper_bound
        """
        if lower_bound >= upper_bound:
            raise ValueError("Requires lowerBound < upperBound.")
        self._lower_bound = lower_bound
        self._upper_bound = upper_bound
    
    def get_lower_bound(self) -> float:
        """Returns the lower bound."""
        return self._lower_bound
    
    def get_upper_bound(self) -> float:
        """Returns the upper bound."""
        return self._upper_bound
    
    def get_paint(self, value: float) -> Tuple[int, int, int]:
        # Validate that value is a number and within bounds
        if value < self._lower_bound or value > self._upper_bound:
            raise ValueError(f"Value {value} outside of bounds [{self._lower_bound}, {self._upper_bound}]")

        # Normalize value to 0..1 within bounds
        range_span = self._upper_bound - self._lower_bound
        if range_span == 0.0:
            # Should not happen because constructor prevents equal bounds, but guard anyway
            normalized = 0.0
        else:
            normalized = (value - self._lower_bound) / range_span

        # Compute gray component 0..255
        g = int(normalized * 255.0)

        # Ensure components are within 0..255
        r = g
        b = g
        out_of_range = []
        if r < 0 or r > 255:
            out_of_range.append(f"r={r}")
        if g < 0 or g > 255:
            out_of_range.append(f"g={g}")
        if b < 0 or b > 255:
            out_of_range.append(f"b={b}")
        if out_of_range:
            raise ValueError(
                f"Color component(s) out of range for value={value} bounds=[{self._lower_bound}, {self._upper_bound}]: "
                + ", ".join(out_of_range)
            )

        return (r, g, b)
    
    def __eq__(self, other) -> bool:
        """
        Tests this GrayPaintScale instance for equality with an arbitrary object.
        """
        if other is self:
            return True
        if not isinstance(other, GrayPaintScale):
            return False
        if self._lower_bound != other._lower_bound:
            return False
        if self._upper_bound != other._upper_bound:
            return False
        return True
    
    def __hash__(self) -> int:
        return hash((self._lower_bound, self._upper_bound))
    
    def clone(self) -> 'GrayPaintScale':
        """Returns a clone of this GrayPaintScale instance."""
        return copy.copy(self)