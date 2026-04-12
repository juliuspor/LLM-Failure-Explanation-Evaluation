def get_paint(self, value: float) -> Tuple[int, int, int]:
    # Clamp input value to bounds
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)

    # Compute normalized fraction safely (denominator is guaranteed non-zero by __init__)
    frac = (v - self._lower_bound) / (self._upper_bound - self._lower_bound)

    # Convert to 0..255 and round to nearest int
    g = int(round(frac * 255.0))

    # Ensure g is within 0..255 (clamp as a final safety)
    if g < 0:
        g = 0
    elif g > 255:
        g = 255

    return (g, g, g)