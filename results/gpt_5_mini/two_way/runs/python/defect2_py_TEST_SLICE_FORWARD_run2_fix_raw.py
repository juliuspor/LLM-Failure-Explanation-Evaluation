def get_paint(self, value: float) -> Tuple[int, int, int]:
    # Clamp value to bounds
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)

    # Normalize clamped value to range 0..255
    span = self._upper_bound - self._lower_bound
    # span should never be zero because constructor enforces lower < upper,
    # but guard defensively to avoid ZeroDivisionError.
    if span == 0.0:
        g = 0
    else:
        g = int((v - self._lower_bound) / span * 255.0)

    # Ensure g is within 0..255 after rounding/truncation
    if g < 0:
        g = 0
    elif g > 255:
        g = 255

    return (g, g, g)