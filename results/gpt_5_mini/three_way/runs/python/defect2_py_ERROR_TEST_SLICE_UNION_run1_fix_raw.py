def get_paint(self, value: float) -> Tuple[int, int, int]:
    # Clamp value to bounds
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)

    # Normalize v to 0..1 over the bounds, then map to 0..255
    ratio = (v - self._lower_bound) / (self._upper_bound - self._lower_bound)
    g = int(round(ratio * 255.0))

    # Ensure integer is within valid RGB range
    if g < 0:
        g = 0
    elif g > 255:
        g = 255

    return (g, g, g)