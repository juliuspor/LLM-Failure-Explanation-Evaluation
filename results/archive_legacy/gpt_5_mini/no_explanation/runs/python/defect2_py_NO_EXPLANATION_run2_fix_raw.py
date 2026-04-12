def get_paint(self, value: float) -> Tuple[int, int, int]:
    # Clamp value to bounds
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)

    # Normalize to 0..255 using the clamped value
    fraction = (v - self._lower_bound) / (self._upper_bound - self._lower_bound)
    g = int(fraction * 255.0)

    # Ensure g is within 0..255 (protect against floating point rounding)
    if g < 0:
        g = 0
    elif g > 255:
        g = 255

    return (g, g, g)