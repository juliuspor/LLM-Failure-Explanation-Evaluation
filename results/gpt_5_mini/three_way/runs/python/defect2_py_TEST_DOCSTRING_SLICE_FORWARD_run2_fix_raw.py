def get_paint(self, value: float) -> Tuple[int, int, int]:
    # Clamp value to bounds
    v = max(self._lower_bound, min(self._upper_bound, value))

    # Compute normalized fraction (safe because constructor ensures lower < upper)
    fraction = (v - self._lower_bound) / (self._upper_bound - self._lower_bound)

    # Convert to 0..255 with rounding
    g = int(round(fraction * 255.0))

    # Ensure within 0..255
    if g < 0:
        g = 0
    elif g > 255:
        g = 255

    return (g, g, g)