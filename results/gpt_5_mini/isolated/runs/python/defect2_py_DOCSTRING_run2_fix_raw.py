def get_paint(self, value: float) -> Tuple[int, int, int]:
    # Clamp value to bounds
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)

    # Compute normalized position as float to avoid integer division issues
    range_span = (self._upper_bound - self._lower_bound)
    if range_span == 0.0:
        t = 0.0
    else:
        t = float(v - self._lower_bound) / float(range_span)

    g = int(t * 255.0)

    # Clamp g just in case of rounding
    if g < 0:
        g = 0
    elif g > 255:
        g = 255

    return (g, g, g)