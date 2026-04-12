def get_paint(self, value: float) -> Tuple[int, int, int]:
    # Clamp value to bounds
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)

    # Normalize to 0..255 and round to nearest integer
    if self._upper_bound == self._lower_bound:
        g = 0
    else:
        g = int(round((v - self._lower_bound) / (self._upper_bound - self._lower_bound) * 255.0))

    # Ensure g is within 0..255
    g = max(0, min(255, g))

    return (g, g, g)