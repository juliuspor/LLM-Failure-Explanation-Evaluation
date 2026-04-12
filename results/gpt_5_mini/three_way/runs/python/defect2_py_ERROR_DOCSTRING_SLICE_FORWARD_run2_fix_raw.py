def get_paint(self, value: float) -> Tuple[int, int, int]:
    # Clamp input value to the bounds
    v = max(self._lower_bound, min(self._upper_bound, value))

    # Guard against division by zero (constructor should prevent this, but be defensive)
    span = self._upper_bound - self._lower_bound
    if span == 0:
        scale = 0.0
    else:
        scale = (v - self._lower_bound) / span

    # Compute gray level, round to nearest int
    g = int(round(scale * 255.0))

    # Ensure within 0..255
    if g < 0:
        g = 0
    elif g > 255:
        g = 255

    return (g, g, g)