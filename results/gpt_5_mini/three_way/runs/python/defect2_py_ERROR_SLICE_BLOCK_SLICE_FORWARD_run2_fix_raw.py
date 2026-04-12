def get_paint(self, value: float) -> Tuple[int, int, int]:
    # Clamp value to bounds
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)

    # Compute gray level based on clamped value
    g_float = (v - self._lower_bound) / (self._upper_bound - self._lower_bound) * 255.0
    g = int(g_float)

    # Validate the range
    if g < 0 or g > 255:
        raise ValueError(f"Color parameter out of range: g={g} (from computed float {g_float})")

    return (g, g, g)