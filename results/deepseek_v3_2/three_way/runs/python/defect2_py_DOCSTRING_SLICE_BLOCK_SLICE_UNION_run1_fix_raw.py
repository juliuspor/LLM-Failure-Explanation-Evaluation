    def get_paint(self, value: float) -> Tuple[int, int, int]:
        """
        Map a numeric value to a grayscale RGB color.

        The input value is interpreted relative to this scale's bounds. Values
        outside the bounds are clamped before conversion.

        Args:
            value: Numeric value to map.
            
        Returns:
            An `(r, g, b)` tuple where all components are equal and in `0..255`.
            
        Raises:
            ValueError: If the computed color components fall outside `0..255`.
        """
        # Clamp value to bounds
        v = max(value, self._lower_bound)
        v = min(v, self._upper_bound)
        
        # Avoid division by zero when bounds are equal.
        if self._upper_bound == self._lower_bound:
            # In this case, all values are clamped to the same point.
            # We can return a fixed gray, e.g., mid-gray (128) or based on value?
            # Since the bounds are equal, the scale is degenerate; any value maps to the same color.
            # The original JFreeChart behavior? It would compute (value - lower) / 0 -> NaN.
            # We'll define that when bounds are equal, the color is black (0) or white? 
            # But the clamp ensures v == lower_bound == upper_bound.
            # Let's follow the logical extreme: the fraction is 0/0, but we can treat as 0.
            # However, the typical use expects a single color. We'll return black (0) for consistency
            # with the case where value <= lower_bound (which gives 0).
            g = 0
        else:
            g = int((v - self._lower_bound) / (self._upper_bound - self._lower_bound) * 255.0)
        
        # In Python, we validate the range (Java Color constructor does this)
        if g < 0 or g > 255:
            raise ValueError(f"Color parameter outside of expected range: Red Green Blue")
        
        return (g, g, g)