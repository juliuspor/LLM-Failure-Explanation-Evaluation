def get_paint(self, value: float) -> Tuple[int, int, int]:
    # Clamp value to bounds
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)

    # Guard against zero denominator (should not occur because __init__ enforces lower < upper)
    denom = (self._upper_bound - self._lower_bound)
    if denom == 0.0:
        # As a fallback, treat as midpoint gray
        g = 127
    else:
        g = int((v - self._lower_bound) / denom * 255.0)

    # Clamp g into valid range 0..255
    if g < 0:
        g = 0
    elif g > 255:
        g = 255

    # Validate and return
    if g < 0 or g > 255:
        raise ValueError(f"Color parameter outside of expected range: {g}")

    return (g, g, g)