def get_paint(self, value: float) -> Tuple[int, int, int]:
    # Clamp value to bounds
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)

    # Defensive: avoid division by zero (constructor should prevent this)
    span = (self._upper_bound - self._lower_bound)
    if span == 0.0:
        g = 0
    else:
        g = int((v - self._lower_bound) / span * 255.0)

    # Clamp g into valid byte range
    if g < 0:
        g = 0
    elif g > 255:
        g = 255

    return (g, g, g)