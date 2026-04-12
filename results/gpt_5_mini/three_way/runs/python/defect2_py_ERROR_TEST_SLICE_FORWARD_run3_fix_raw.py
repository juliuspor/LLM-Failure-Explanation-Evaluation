def get_paint(self, value: float) -> Tuple[int, int, int]:
    # Clamp input value to bounds
    v = max(self._lower_bound, min(self._upper_bound, value))

    # Avoid division by zero (shouldn't happen because constructor enforces lower < upper)
    range_span = self._upper_bound - self._lower_bound
    if range_span == 0.0:
        fraction = 0.0
    else:
        fraction = (v - self._lower_bound) / range_span

    # Compute gray level, convert to int and clamp to 0..255
    g = int(round(fraction * 255.0))
    g = max(0, min(255, g))

    return (g, g, g)