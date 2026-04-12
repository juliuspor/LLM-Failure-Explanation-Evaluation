def get_paint(self, value: float) -> Tuple[int, int, int]:
    # Clamp value to bounds
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)

    # Compute normalized ratio using the clamped value and clamp to [0.0, 1.0]
    ratio = (v - self._lower_bound) / (self._upper_bound - self._lower_bound)
    if ratio < 0.0:
        ratio = 0.0
    elif ratio > 1.0:
        ratio = 1.0

    g = int(ratio * 255.0)

    # Ensure g is within 0..255 (safety)
    if g < 0 or g > 255:
        raise ValueError("Color parameter outside of expected range: Red Green Blue")

    return (g, g, g)