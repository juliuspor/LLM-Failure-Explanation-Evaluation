def get_paint(self, value: float) -> Tuple[int, int, int]:
    # Clamp value to bounds
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)

    # Compute gray level based on the clamped value
    ratio = (v - self._lower_bound) / (self._upper_bound - self._lower_bound)
    g = int(ratio * 255.0)

    # Clamp to valid 0..255 range to be safe
    if g < 0:
        g = 0
    elif g > 255:
        g = 255

    return (g, g, g)