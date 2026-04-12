def get_paint(self, value: float) -> Tuple[int, int, int]:
    lb = self._lower_bound
    ub = self._upper_bound
    v = max(value, lb)
    v = min(v, ub)
    ratio = (v - lb) / (ub - lb)
    g = int(round(ratio * 255.0))
    g = max(0, min(255, g))
    return (g, g, g)