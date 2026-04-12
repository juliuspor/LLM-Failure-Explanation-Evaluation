def get_paint(self, value: float) -> Tuple[int, int, int]:
    # Clamp value to bounds
    v = max(self._lower_bound, min(value, self._upper_bound))

    # Guard against division by zero (shouldn't occur because constructor enforces bounds)
    range_span = self._upper_bound - self._lower_bound
    if range_span == 0.0:
        raise ValueError("Invalid scale with lower_bound equal to upper_bound")

    # Compute gray level from clamped value
    g = int((v - self._lower_bound) / range_span * 255.0)

    # Sanity clamp to 0..255 to avoid any rounding edge cases
    if g < 0:
        g = 0
    elif g > 255:
        g = 255

    return (g, g, g)