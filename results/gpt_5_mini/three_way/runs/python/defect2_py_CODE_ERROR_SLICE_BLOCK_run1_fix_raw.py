def get_paint(self, value: float) -> Tuple[int, int, int]:
    # Clamp value to bounds
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)

    # Guard against zero range (shouldn't happen because constructor enforces lower < upper)
    range_span = self._upper_bound - self._lower_bound
    if range_span == 0:
        g = 0
    else:
        g = int((v - self._lower_bound) / range_span * 255.0)

    # Validate the range
    if g < 0 or g > 255:
        raise ValueError(f"Color parameter outside of expected range: {g}")

    return (g, g, g)