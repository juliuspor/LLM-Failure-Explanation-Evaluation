def get_paint(self, value: float) -> Tuple[int, int, int]:
    # Ensure the scale has a non-zero span
    span = self._upper_bound - self._lower_bound
    if span == 0.0:
        raise ValueError("GrayPaintScale has zero span (upper_bound == lower_bound)")

    # Clamp value to bounds
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)

    # Compute gray level using the clamped value
    g = int((v - self._lower_bound) / span * 255.0)

    # Clamp g to valid RGB range to be defensive
    if g < 0:
        g = 0
    elif g > 255:
        g = 255

    return (g, g, g)