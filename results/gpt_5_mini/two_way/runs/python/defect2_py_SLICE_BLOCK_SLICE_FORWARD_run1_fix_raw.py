def get_paint(self, value: float) -> Tuple[int, int, int]:
    # Clamp value to bounds
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)

    g = int((v - self._lower_bound) / (self._upper_bound - self._lower_bound) * 255.0)

    # In Python, we validate the range (Java Color constructor does this)
    if g < 0 or g > 255:
        raise ValueError(f"Color parameter 'g' outside of expected range 0..255: g={g} (checked at line 77)")

    return (g, g, g)