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
        # Validate input type
        try:
            # Attempt numeric operations to catch None/NaN early (NaN handled below)
            _ = float(value)
        except Exception:
            raise TypeError("value must be a numeric type")

        # Clamp value to bounds using the bounds stored on the instance
        v = max(value, self._lower_bound)
        v = min(v, self._upper_bound)

        # Guard against zero range
        range_span = self._upper_bound - self._lower_bound
        if range_span == 0.0:
            raise ValueError("Lower and upper bounds must not be equal")

        # Compute normalized intensity in [0.0, 1.0]
        intensity = (v - self._lower_bound) / float(range_span)
        # Clamp intensity robustly
        intensity = max(0.0, min(1.0, intensity))

        # Convert to 0..255 using rounding to avoid 256 due to floating point
        g = int(round(intensity * 255.0))
        # Final clamp to ensure within 0..255
        g = max(0, min(255, g))

        return (g, g, g)
    
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