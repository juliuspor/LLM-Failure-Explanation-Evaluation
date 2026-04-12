def get_paint(self, value: float) -> Tuple[int, int, int]:
    # Clamp value to bounds
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)

    # Avoid division by zero if bounds are equal (shouldn't happen due to ctor check,
    # but guard defensively)
    span = (self._upper_bound - self._lower_bound)
    if span == 0:
        g = 127
    else:
        g = int((v - self._lower_bound) / span * 255.0)

    # Clamp g to valid byte range
    if g < 0:
        g = 0
    elif g > 255:
        g = 255

    return (g, g, g)
