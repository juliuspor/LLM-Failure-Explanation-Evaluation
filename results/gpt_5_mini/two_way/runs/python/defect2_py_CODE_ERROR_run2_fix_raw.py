def get_paint(self, value: float) -> Tuple[int, int, int]:
    # Clamp value to bounds
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)

    range_span = (self._upper_bound - self._lower_bound)
    if range_span == 0.0:
        # Degenerate case: bounds are equal; return mid-gray
        g = 128
    else:
        g = int((v - self._lower_bound) / range_span * 255.0)

    if g < 0 or g > 255:
        raise ValueError(f"Color component outside of expected range: {g}")

    return (g, g, g)