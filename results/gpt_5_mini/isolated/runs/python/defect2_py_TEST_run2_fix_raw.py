def get_paint(self, value: float) -> Tuple[int, int, int]:
    # Clamp value to bounds
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)

    # Normalize clamped value to [0.0, 1.0]
    range_span = self._upper_bound - self._lower_bound
    if range_span == 0.0:
        # Should not happen because constructor enforces lower < upper,
        # but guard against division by zero defensively.
        frac = 0.0
    else:
        frac = (v - self._lower_bound) / range_span

    # Scale to 0..255 using int() to truncate toward zero
    g = int(frac * 255.0)

    # Ensure value is within byte range
    if g < 0 or g > 255:
        raise ValueError("Color parameter outside of expected range: Red Green Blue")

    return (g, g, g)