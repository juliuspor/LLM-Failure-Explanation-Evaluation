def get_paint(self, value: float) -> Tuple[int, int, int]:
    # Clamp value to bounds
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)

    # Compute gray level scaled to 0..255. Use rounding to map midpoints as expected.
    ratio = (v - self._lower_bound) / (self._upper_bound - self._lower_bound)
    g = int(round(ratio * 255.0))

    # Ensure g is within 0..255 (defensive)
    if g < 0:
        g = 0
    elif g > 255:
        g = 255

    return (g, g, g)