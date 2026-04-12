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
        # Clamp value to bounds
        v = max(value, self._lower_bound)
        v = min(v, self._upper_bound)

        # Compute normalized fraction using clamped v to avoid issues and ensure consistent results
        denom = (self._upper_bound - self._lower_bound)
        if denom == 0.0:
            # Defensive: if bounds were equal (should be prevented by constructor), treat as middle gray
            g = 128
        else:
            frac = (v - self._lower_bound) / denom
            g = int(frac * 255.0)

        # Clamp g to valid byte range
        if g < 0:
            g = 0
        elif g > 255:
            g = 255

        # Validate and provide helpful error if something unexpected occurred
        if g < 0 or g > 255:
            raise ValueError(f"Color parameter outside of expected range: g={g}, value={value}")

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