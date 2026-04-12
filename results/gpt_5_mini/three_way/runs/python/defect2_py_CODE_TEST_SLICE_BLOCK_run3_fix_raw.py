def get_paint(self, value: float) -> Tuple[int, int, int]:
    # Clamp value to bounds
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)

    range_span = self._upper_bound - self._lower_bound
    if range_span == 0.0:
        # Avoid division by zero; treat as mid-gray
        normalized = 0.5
    else:
        normalized = (v - self._lower_bound) / range_span

    # Scale to 0..255 and ensure within bounds before converting to int
    g_float = normalized * 255.0
    g_clamped = min(max(g_float, 0.0), 255.0)
    g = int(g_clamped)

    if g < 0 or g > 255:
        raise ValueError(f"Color parameter outside of expected range: Red Green Blue")

    return (g, g, g)