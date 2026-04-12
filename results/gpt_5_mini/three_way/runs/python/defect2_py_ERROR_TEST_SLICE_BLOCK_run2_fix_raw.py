def get_paint(self, value: float) -> Tuple[int, int, int]:
    # Clamp value to bounds
    v = max(self._lower_bound, min(self._upper_bound, value))

    # Avoid division by zero (should not occur because constructor enforces lower < upper)
    range_span = self._upper_bound - self._lower_bound
    if range_span == 0.0:
        fraction = 0.0
    else:
        fraction = (v - self._lower_bound) / range_span

    g = int(fraction * 255.0)

    # Clamp g to valid RGB range
    if g < 0:
        g = 0
    elif g > 255:
        g = 255

    # Sanity check (should not raise if clamped correctly)
    if g < 0 or g > 255:
        raise ValueError("Color parameter outside of expected range: Red Green Blue")

    return (g, g, g)