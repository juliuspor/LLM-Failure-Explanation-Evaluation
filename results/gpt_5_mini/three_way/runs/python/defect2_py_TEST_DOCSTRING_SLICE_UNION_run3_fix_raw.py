def get_paint(self, value: float) -> Tuple[int, int, int]:
    # Clamp value to bounds
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)

    # Compute fraction within bounds and convert to 0..255 gray
    fraction = (v - self._lower_bound) / (self._upper_bound - self._lower_bound)
    g = int(fraction * 255.0)

    # Ensure g is within valid RGB range
    g = max(0, min(255, g))

    return (g, g, g)