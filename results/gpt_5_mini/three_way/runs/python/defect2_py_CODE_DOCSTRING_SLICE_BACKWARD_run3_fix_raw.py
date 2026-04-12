def get_paint(self, value: float) -> Tuple[int, int, int]:
    # Clamp value to bounds
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)

    # Compute normalized position within bounds; denominator should not be zero
    denom = (self._upper_bound - self._lower_bound)
    if denom == 0.0:
        raise ValueError("Invalid paint scale with zero range.")

    g = int((v - self._lower_bound) / denom * 255.0)

    # Ensure g is within valid byte range
    if g < 0:
        g = 0
    elif g > 255:
        g = 255

    return (g, g, g)