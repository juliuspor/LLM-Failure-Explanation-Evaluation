def get_paint(self, value: float) -> Tuple[int, int, int]:
    # Clamp value to bounds
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)

    # Compute normalized position using the clamped value
    span = (self._upper_bound - self._lower_bound)
    if span == 0.0:
        # Should not happen because constructor prevents this, but be defensive
        gray = 0
    else:
        gray = int((v - self._lower_bound) / span * 255.0)

    # Clamp the resulting component to valid 0..255 range
    if gray < 0:
        gray = 0
    elif gray > 255:
        gray = 255

    return (gray, gray, gray)