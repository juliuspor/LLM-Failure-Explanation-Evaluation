def get_paint(self, value: float) -> Tuple[int, int, int]:
    # Clamp value to bounds
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)

    range_span = (self._upper_bound - self._lower_bound)
    if range_span == 0.0:
        raise ValueError("Invalid paint scale range: lower_bound == upper_bound")

    # Compute normalized ratio using the clamped value
    ratio = (v - self._lower_bound) / range_span
    # Ensure ratio is within [0.0, 1.0]
    if ratio < 0.0:
        ratio = 0.0
    elif ratio > 1.0:
        ratio = 1.0

    g = int(ratio * 255.0)

    # Clamp g to valid byte range just in case
    if g < 0:
        g = 0
    elif g > 255:
        g = 255

    return (g, g, g)