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
        
        # Compute grayscale component
        gray = int((v - self._lower_bound) / (self._upper_bound - self._lower_bound) * 255.0)
        
        # Validate the range
        if gray < 0 or gray > 255:
            raise ValueError(f"Color parameter outside of expected range: {gray}")
        
        return (gray, gray, gray)