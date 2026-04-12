def get_paint(self, value: float) -> Tuple[int, int, int]:
    # Clamp input to bounds
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)

    # Compute fraction relative to bounds using the clamped value
    fraction = (v - self._lower_bound) / (self._upper_bound - self._lower_bound)

    # Convert to an integer gray level in 0..255, rounding to nearest
    g = int(fraction * 255.0 + 0.5)

    # Ensure g is within valid range
    if g < 0 or g > 255:
        raise ValueError(f"Color parameter outside of expected range: {g}")

    return (g, g, g)