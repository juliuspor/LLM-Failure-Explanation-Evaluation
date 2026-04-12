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
        
        # Compute grayscale component as a float in [0, 255]
        g_float = (v - self._lower_bound) / (self._upper_bound - self._lower_bound) * 255.0
        # Clamp to [0, 255] to avoid out-of-range due to floating point errors or extreme bounds
        g_clamped = max(0.0, min(g_float, 255.0))
        g = int(round(g_clamped))
        # Ensure integer is within bounds (should be, but double-check)
        if g < 0 or g > 255:
            raise ValueError(f"Color parameter outside of expected range: Red Green Blue")
        
        return (g, g, g)