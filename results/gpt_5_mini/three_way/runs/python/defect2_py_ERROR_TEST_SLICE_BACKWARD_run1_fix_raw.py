def get_paint(self, value: float) -> Tuple[int, int, int]:
    # Clamp value to bounds
    v = max(self._lower_bound, min(value, self._upper_bound))

    # Compute gray level as an integer in 0..255
    fraction = (v - self._lower_bound) / (self._upper_bound - self._lower_bound)
    g = int(round(fraction * 255.0))

    # Ensure g is within bounds (defensive programming)
    if g < 0:
        g = 0
    elif g > 255:
        g = 255

    return (g, g, g)