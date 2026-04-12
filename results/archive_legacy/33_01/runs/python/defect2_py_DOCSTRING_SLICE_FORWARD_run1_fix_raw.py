def get_paint(self, value: float) -> Tuple[int, int, int]:
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)
    ratio = (v - self._lower_bound) / (self._upper_bound - self._lower_bound)
    g = int(round(ratio * 255.0))
    if not (0 <= g <= 255):
        raise ValueError(f"RGB component out of range: {g}")
    return (g, g, g)