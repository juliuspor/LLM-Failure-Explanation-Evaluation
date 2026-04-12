def get_paint(self, value: float) -> Tuple[int, int, int]:
    # Clamp value to bounds
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)

    # Compute gray level based on clamped value
    # Safe because constructor ensures lower < upper
    fraction = (v - self._lower_bound) / (self._upper_bound - self._lower_bound)
    g = int(fraction * 255.0)

    # Validate range
    if g < 0 or g > 255:
        raise ValueError(f"Color parameter out of range for gray component: {g} (expected 0..255)")

    return (g, g, g)