def get_paint(self, value: float) -> Tuple[int, int, int]:
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)
    g = int((v - self._lower_bound) / (self._upper_bound - self._lower_bound) * 255.0)
    r = g
    b = g
    for name, val in (("r", r), ("g", g), ("b", b)):
        if not isinstance(val, int):
            raise TypeError(f"Color parameter must be int: {name}={val!r}")
        if val < 0 or val > 255:
            raise ValueError(f"Color parameter outside of expected range: {name}={val}")
    return (r, g, b)