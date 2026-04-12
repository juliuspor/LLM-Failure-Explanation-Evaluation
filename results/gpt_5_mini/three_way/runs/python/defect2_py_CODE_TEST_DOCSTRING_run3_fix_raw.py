def get_paint(self, value: float) -> Tuple[int, int, int]:
    # Clamp value to bounds
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)

    # Defensive: avoid division by zero (constructor should prevent this)
    range_span = (self._upper_bound - self._lower_bound)
    if range_span == 0.0:
        g = 0
    else:
        # Use the clamped value 'v' to compute the gray level
        g = int(round((v - self._lower_bound) / range_span * 255.0))

    # Ensure g is within 0..255
    if g < 0:
        g = 0
    elif g > 255:
        g = 255

    return (g, g, g)