def get_paint(self, value: float) -> Tuple[int, int, int]:
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)
    g = int((v - self._lower_bound) / (self._upper_bound - self._lower_bound) * 255.0)
    r = g
    b = g
    for name, val in (('r', r), ('g', g), ('b', b)):
        if val < 0 or val > 255:
            raise ValueError(f"Color parameter out of range: {name}={val}")
    return (r, g, b)