def get_paint(self, value: float) -> Tuple[int, int, int]:
    # Clamp value to bounds
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)

    span = self._upper_bound - self._lower_bound
    if span == 0.0:
        raise ValueError("GrayPaintScale has zero range (lower_bound == upper_bound)")

    normalized = (v - self._lower_bound) / span
    # Ensure normalized is within [0.0, 1.0]
    normalized = max(0.0, min(1.0, normalized))

    g = int(round(normalized * 255.0))

    # Validate range (mirrors Java Color constructor behavior)
    if g < 0 or g > 255:
        raise ValueError(f"Color parameter outside of expected range: {g}")

    return (g, g, g)
