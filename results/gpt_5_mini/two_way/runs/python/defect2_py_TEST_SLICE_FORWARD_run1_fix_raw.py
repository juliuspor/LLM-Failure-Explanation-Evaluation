def get_paint(self, value: float) -> Tuple[int, int, int]:
    # Clamp value to bounds
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)

    # Compute fraction in [0.0, 1.0] using the clamped value
    fraction = (v - self._lower_bound) / (self._upper_bound - self._lower_bound)

    # Map to 0..255 and round to nearest integer
    g = int(round(fraction * 255.0))

    # Ensure within bounds (protect against rounding issues)
    if g < 0:
        g = 0
    elif g > 255:
        g = 255

    return (g, g, g)