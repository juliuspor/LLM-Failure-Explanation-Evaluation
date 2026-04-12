def get_paint(self, value: float) -> Tuple[int, int, int]:
    if self._upper_bound == self._lower_bound:
        raise ValueError(f"get_paint: upper_bound ({self._upper_bound}) equals lower_bound ({self._lower_bound})")
    if self._upper_bound < self._lower_bound:
        raise ValueError(f"get_paint: upper_bound ({self._upper_bound}) < lower_bound ({self._lower_bound})")
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)
    ratio = (v - self._lower_bound) / (self._upper_bound - self._lower_bound)
    ratio = max(0.0, min(1.0, ratio))
    g = int(round(ratio * 255.0))
    return (g, g, g)