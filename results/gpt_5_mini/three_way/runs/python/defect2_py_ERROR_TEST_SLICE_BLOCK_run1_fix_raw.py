def get_paint(self, value: float) -> Tuple[int, int, int]:
    # Clamp input value to bounds
    t = max(self._lower_bound, min(self._upper_bound, value))

    # Compute gray level in 0..255. Use int() to match expected rounding (floor)
    g_float = (t - self._lower_bound) / (self._upper_bound - self._lower_bound) * 255.0
    g = int(g_float)

    # Clamp g to valid 0..255 range
    g = max(0, min(255, g))

    return (g, g, g)