def get_paint(self, value: float) -> Tuple[int, int, int]:
    # Clamp input value to bounds first
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)

    # Normalize to 0..1 using the clamped value
    denom = (self._upper_bound - self._lower_bound)
    if denom == 0:
        # Should not happen because constructor enforces bounds, but guard anyway
        value_norm = 0.0
    else:
        value_norm = (v - self._lower_bound) / denom

    # Scale to 0..255 and round to nearest integer
    g = int(round(value_norm * 255.0))

    # Clamp final component to valid byte range to guard against floating-point
    if g < 0:
        g = 0
    elif g > 255:
        g = 255

    return (g, g, g)