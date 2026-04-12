def get_paint(self, value: float) -> Tuple[int, int, int]:
    # Clamp value to bounds
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)

    # Safely compute fraction; guard against zero division just in case
    span = (self._upper_bound - self._lower_bound)
    if span == 0.0:
        fraction = 0.0
    else:
        fraction = (v - self._lower_bound) / span

    # Map to 0-255 and ensure integer in range
    g = int(round(fraction * 255.0))

    # Clamp g to valid range to avoid unexpected errors
    if g < 0 or g > 255:
        raise ValueError(f"Color component out of range: g={g} (expected 0..255)")

    return (g, g, g)
