def get_paint(self, value: float) -> Tuple[int, int, int]:
    # Clamp value to bounds
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)

    denom = (self._upper_bound - self._lower_bound)
    if denom == 0.0:
        # Defensive: should not happen because __init__ prevents equal bounds
        g = 0
    else:
        g = int((v - self._lower_bound) / denom * 255.0)

    # Validate the computed gray component
    if g < 0 or g > 255:
        raise ValueError(f"Color parameter outside expected range: g={g} (expected 0..255)")

    return (g, g, g)