def get_paint(self, value: float) -> Tuple[int, int, int]:
    # Clamp value to bounds
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)

    # Normalize into [0.0, 1.0]
    span = self._upper_bound - self._lower_bound
    if span == 0.0:
        normalized = 0.0
    else:
        normalized = (v - self._lower_bound) / span

    # Map to 0..255, using floor so that 0.5 -> 127 (since 0.5*255 = 127.5)
    import math
    g = int(math.floor(normalized * 255.0))

    # Clamp to integer 0..255
    if g < 0:
        g = 0
    elif g > 255:
        g = 255

    return (g, g, g)