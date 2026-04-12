def get_paint(self, value: float) -> Tuple[int, int, int]:
    # Clamp value to bounds before computing ratio
    v = max(self._lower_bound, min(self._upper_bound, value))

    # Compute ratio in [0.0, 1.0]
    ratio = (v - self._lower_bound) / (self._upper_bound - self._lower_bound)

    # Convert to 0..255 and round to nearest int
    g = int(round(ratio * 255.0))

    # Ensure within valid RGB range
    if g < 0:
        g = 0
    elif g > 255:
        g = 255

    return (g, g, g)