def get_paint(self, value: float) -> Tuple[int, int, int]:
    # Ensure bounds are valid
    if self._upper_bound == self._lower_bound:
        raise ValueError("Invalid scale bounds: upper_bound must be different from lower_bound")

    # Clamp value to bounds
    v = max(self._lower_bound, min(value, self._upper_bound))

    # Compute gray level as a float in 0..255
    ratio = (v - self._lower_bound) / (self._upper_bound - self._lower_bound)
    g_float = ratio * 255.0

    # Round to nearest integer and clamp to valid RGB range
    g = int(round(g_float))
    g = max(0, min(255, g))

    return (g, g, g)