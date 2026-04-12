def get_paint(self, value: float) -> Tuple[int, int, int]:
    # Clamp value to bounds
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)

    denom = (self._upper_bound - self._lower_bound)
    if denom == 0.0:
        # Defensive: should not happen because __init__ prevents equal bounds
        g = 0
    else:
        # Normalize clamped value and map to 0..255
        g = int((v - self._lower_bound) / denom * 255.0)

    # Validate range
    if g < 0 or g > 255:
        raise ValueError(f"Color parameter outside of expected range: Gray={g}")

    return (g, g, g)