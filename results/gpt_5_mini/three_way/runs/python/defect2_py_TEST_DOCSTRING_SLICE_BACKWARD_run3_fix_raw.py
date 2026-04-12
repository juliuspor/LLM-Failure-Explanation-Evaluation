def get_paint(self, value: float) -> Tuple[int, int, int]:
    # Clamp value to bounds
    v = max(self._lower_bound, min(value, self._upper_bound))

    g = int((v - self._lower_bound) / (self._upper_bound - self._lower_bound) * 255.0)

    # Ensure g is within 0..255 (should be guaranteed by clamping, but guard defensively)
    if g < 0:
        g = 0
    elif g > 255:
        g = 255

    return (g, g, g)