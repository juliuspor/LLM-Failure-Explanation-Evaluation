def get_paint(self, value: float) -> Tuple[int, int, int]:
    # Clamp value to bounds
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)

    range_span = self._upper_bound - self._lower_bound
    if range_span == 0.0:
        fraction = 0.0
    else:
        fraction = (v - self._lower_bound) / range_span

    # Ensure fraction is within [0,1]
    if fraction < 0.0:
        fraction = 0.0
    elif fraction > 1.0:
        fraction = 1.0

    g = int(round(fraction * 255.0))

    # Validate range
    if g < 0 or g > 255:
        raise ValueError("Color parameter outside of expected range: Red Green Blue")

    return (g, g, g)