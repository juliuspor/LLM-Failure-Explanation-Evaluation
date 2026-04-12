def get_paint(self, value: float) -> Tuple[int, int, int]:
    # Clamp input value to bounds
    v = max(self._lower_bound, min(value, self._upper_bound))

    # Prevent division by zero (shouldn't happen because constructor enforces bounds,
    # but be defensive)
    span = (self._upper_bound - self._lower_bound)
    if span == 0.0:
        g = 127
    else:
        g = int((v - self._lower_bound) / span * 255.0)

    # Clamp g to valid RGB range
    g = max(0, min(g, 255))

    return (g, g, g)