def get_paint(self, value: float) -> Tuple[int, int, int]:
    if self._upper_bound == self._lower_bound:
        raise ValueError(f"Invalid bounds: upper_bound ({self._upper_bound}) == lower_bound ({self._lower_bound})")
    v = max(self._lower_bound, min(value, self._upper_bound))
    fraction = (v - self._lower_bound) / (self._upper_bound - self._lower_bound)
    g = int(round(fraction * 255.0))
    g = max(0, min(255, g))
    return (g, g, g)