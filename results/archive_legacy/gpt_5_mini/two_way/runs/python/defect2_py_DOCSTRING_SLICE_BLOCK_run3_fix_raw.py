def get_paint(self, value: float) -> Tuple[int, int, int]:
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)
    if self._upper_bound == self._lower_bound:
        g = 0
    else:
        g = int(round((v - self._lower_bound) / (self._upper_bound - self._lower_bound) * 255.0))
    r = g
    b = g
    bad = [(name, val) for name, val in (("r", r), ("g", g), ("b", b)) if not (0 <= val <= 255)]
    if bad:
        raise ValueError("Color parameter(s) out of range: " + ", ".join(f"{n}={v}" for n, v in bad))
    return (r, g, b)