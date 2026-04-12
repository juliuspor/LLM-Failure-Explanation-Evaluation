def get_paint(self, value: float) -> Tuple[int, int, int]:
    # Ensure denominator is not zero (constructor prevents equal bounds, but guard defensively)
    range_span = self._upper_bound - self._lower_bound
    if range_span == 0.0:
        raise ValueError("GrayPaintScale has zero range (upper_bound == lower_bound)")

    # Clamp input value to bounds before computing the gray level
    v = max(self._lower_bound, min(value, self._upper_bound))

    # Normalize to [0.0, 1.0] and scale to [0, 255]
    fraction = (v - self._lower_bound) / range_span
    g_float = fraction * 255.0
    # Use round to reduce truncation bias, then cast to int
    g = int(round(g_float))

    # Ensure g is within valid RGB range
    if g < 0 or g > 255:
        raise ValueError(f"Computed gray component out of range: {g}")

    return (g, g, g)