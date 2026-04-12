def get_paint(self, value: float) -> Tuple[int, int, int]:
    # Clamp value to bounds
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)

    # Normalize within [0.0, 1.0]
    normalized = (v - self._lower_bound) / (self._upper_bound - self._lower_bound)

    # Map to 0..255 using truncation
    g = int(normalized * 255.0)

    # Ensure g is within byte range
    if g < 0 or g > 255:
        raise ValueError("Color parameter outside of expected range: Red Green Blue")

    return (g, g, g)