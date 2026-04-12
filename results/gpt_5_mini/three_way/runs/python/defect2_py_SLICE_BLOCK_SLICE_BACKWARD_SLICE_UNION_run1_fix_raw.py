def get_paint(self, value: float) -> Tuple[int, int, int]:
    # Clamp value to bounds to avoid producing out-of-range gray levels
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)

    # Normalize v to [0.0, 1.0]
    ratio = (v - self._lower_bound) / (self._upper_bound - self._lower_bound)

    # Scale to 0..255 and convert to int
    g = int(ratio * 255.0)

    # Defensive clamp to ensure within byte range
    if g < 0:
        g = 0
    elif g > 255:
        g = 255

    return (g, g, g)