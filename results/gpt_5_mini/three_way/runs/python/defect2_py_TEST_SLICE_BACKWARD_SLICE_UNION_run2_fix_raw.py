def get_paint(self, value: float) -> Tuple[int, int, int]:
    # Clamp value to bounds
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)

    range_ = self._upper_bound - self._lower_bound
    if range_ == 0.0:
        fraction = 0.0
    else:
        fraction = (v - self._lower_bound) / range_

    # Clamp fraction to [0.0, 1.0]
    if fraction < 0.0:
        fraction = 0.0
    elif fraction > 1.0:
        fraction = 1.0

    # Compute gray level and ensure it's within 0..255
    g = int(round(fraction * 255.0))
    if g < 0:
        g = 0
    elif g > 255:
        g = 255

    return (g, g, g)