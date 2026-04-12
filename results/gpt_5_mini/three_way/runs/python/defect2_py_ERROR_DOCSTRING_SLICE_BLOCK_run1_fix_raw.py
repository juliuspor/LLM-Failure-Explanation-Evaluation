def get_paint(self, value: float) -> Tuple[int, int, int]:
    # Clamp value to bounds
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)

    # Normalize v within bounds to [0.0, 1.0]
    span = (self._upper_bound - self._lower_bound)
    if span == 0:
        # Shouldn't happen because constructor enforces bounds, but guard anyway
        normalized = 0.0
    else:
        normalized = (v - self._lower_bound) / span

    # Map to 0..255 and convert to integer
    g = int(normalized * 255.0)

    # Clamp g to integer 0..255 to guard against rounding issues
    if g < 0:
        g = 0
    elif g > 255:
        g = 255

    # Validate range
    if g < 0 or g > 255:
        raise ValueError(f"Color parameter out of range: g={g}")

    return (g, g, g)