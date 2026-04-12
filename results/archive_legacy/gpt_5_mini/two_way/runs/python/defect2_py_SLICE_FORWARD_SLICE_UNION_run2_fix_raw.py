def get_paint(self, value: float) -> Tuple[int, int, int]:
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)
    if self._upper_bound == self._lower_bound:
        g = 128
        return (g, g, g)
    frac = (v - self._lower_bound) / (self._upper_bound - self._lower_bound)
    g = int(round(frac * 255.0))
    if g < 0 or g > 255:
        raise ValueError(f"value {value} out of bounds [{self._lower_bound}, {self._upper_bound}] produced g={g}")
    return (g, g, g)