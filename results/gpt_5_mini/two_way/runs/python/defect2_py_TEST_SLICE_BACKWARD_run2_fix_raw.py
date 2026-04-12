def get_paint(self, value: float) -> Tuple[int, int, int]:
    # Clamp value to bounds
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)

    # Guard against division by zero just in case
    range_span = (self._upper_bound - self._lower_bound)
    if range_span == 0:
        g = 0
    else:
        g = int((v - self._lower_bound) / range_span * 255.0)

    # Clamp g to the valid 0..255 range instead of raising
    if g < 0:
        g = 0
    elif g > 255:
        g = 255

    return (g, g, g)