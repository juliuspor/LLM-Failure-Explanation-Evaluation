def get_paint(self, value: float) -> Tuple[int, int, int]:
    # Clamp value to bounds
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)

    # Defensive check to avoid division by zero
    range_width = self._upper_bound - self._lower_bound
    if range_width == 0.0:
        # Should not happen because constructor enforces lower < upper, but handle defensively
        g = 0
    else:
        g = int((v - self._lower_bound) / range_width * 255.0)

    # In Python, we validate the range (Java Color constructor does this)
    if g < 0 or g > 255:
        raise ValueError(f"Color parameter outside of expected range: {g}")

    return (g, g, g)