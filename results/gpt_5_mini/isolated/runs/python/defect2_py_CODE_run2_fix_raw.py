def get_paint(self, value: float) -> Tuple[int, int, int]:
    # Clamp value to bounds
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)

    # Guard against zero range (shouldn't happen because constructor enforces bounds),
    # but protect against division by zero just in case.
    range_span = (self._upper_bound - self._lower_bound)
    if range_span == 0.0:
        g = 0
    else:
        g = int(round((v - self._lower_bound) / range_span * 255.0))

    # Validate the range
    if g < 0 or g > 255:
        raise ValueError("Color parameter outside of expected range: Red Green Blue")

    return (g, g, g)