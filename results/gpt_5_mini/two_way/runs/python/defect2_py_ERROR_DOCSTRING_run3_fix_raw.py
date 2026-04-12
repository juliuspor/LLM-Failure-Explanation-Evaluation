def get_paint(self, value: float) -> Tuple[int, int, int]:
    # Clamp input value to the configured bounds
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)

    # Normalize to 0.0..1.0 using clamped value
    range_span = self._upper_bound - self._lower_bound
    if range_span == 0.0:
        normalized = 0.0
    else:
        normalized = (v - self._lower_bound) / range_span

    # Ensure normalized is within [0.0, 1.0]
    if normalized < 0.0:
        normalized = 0.0
    elif normalized > 1.0:
        normalized = 1.0

    # Scale to 0..255 and round to nearest integer
    g = int(round(normalized * 255.0))

    # Final clamp to integer byte range
    if g < 0:
        g = 0
    elif g > 255:
        g = 255

    return (g, g, g)