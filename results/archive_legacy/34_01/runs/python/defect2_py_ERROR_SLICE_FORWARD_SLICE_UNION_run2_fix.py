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
        if self._upper_bound == self._lower_bound:
            raise ValueError(f"upper_bound equals lower_bound: {self._upper_bound}")
        v = max(value, self._lower_bound)
        v = min(v, self._upper_bound)
        ratio = (v - self._lower_bound) / (self._upper_bound - self._lower_bound)
        g = int(round(ratio * 255.0))
        if g < 0:
            g = 0
        if g > 255:
            g = 255
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
