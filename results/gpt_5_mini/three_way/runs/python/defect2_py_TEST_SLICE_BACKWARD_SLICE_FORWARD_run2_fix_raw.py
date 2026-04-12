def get_paint(self, value: float) -> Tuple[int, int, int]:
    # Clamp value to bounds
    v = max(self._lower_bound, min(value, self._upper_bound))

    # Protect against division by zero (shouldn't occur because constructor forbids equal bounds)
    range_span = self._upper_bound - self._lower_bound
    if range_span == 0.0:
        g = 0
    else:
        fraction = (v - self._lower_bound) / range_span
        g = int(fraction * 255.0)

    # Ensure g is within 0..255
    if g < 0:
        g = 0
    elif g > 255:
        g = 255

    return (g, g, g)