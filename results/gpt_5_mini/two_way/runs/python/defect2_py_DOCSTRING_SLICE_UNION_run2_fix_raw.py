def get_paint(self, value: float) -> Tuple[int, int, int]:
    # Ensure the scale has a non-zero span
    span = self._upper_bound - self._lower_bound
    if span == 0.0:
        raise ValueError("GrayPaintScale has zero span (upper_bound == lower_bound)")

    # Clamp the input value to the scale bounds
    v = max(self._lower_bound, min(value, self._upper_bound))

    # Compute the gray level as an integer in 0..255
    fraction = (v - self._lower_bound) / span
    g = int(round(fraction * 255.0))

    # Validate range (mirror Java Color constructor behavior)
    if g < 0 or g > 255:
        raise ValueError(f"Color parameter outside of expected range: {g}")

    return (g, g, g)