def get_paint(self, value: float) -> Tuple[int, int, int]:
    # Clamp value to bounds
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)

    # Normalize clamped value to 0..1
    scale = (v - self._lower_bound) / (self._upper_bound - self._lower_bound)

    # Convert to 0..255 integer
    g = int(scale * 255.0)

    # Validate range (safety check)
    if g < 0 or g > 255:
        raise ValueError("Color parameter outside of expected range: Red Green Blue")

    return (g, g, g)