def get_paint(self, value: float) -> Tuple[int, int, int]:
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)
    span = self._upper_bound - self._lower_bound
    if span == 0.0:
        raise ValueError("upper_bound and lower_bound must differ")
    g = int((v - self._lower_bound) / span * 255.0)
    if g < 0 or g > 255:
        raise ValueError(f"Color components out of range: r={g}, g={g}, b={g}")
    return (g, g, g)