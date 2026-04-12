def get_paint(self, value: float) -> Tuple[int, int, int]:
    v = value
    if not isinstance(v, (int, float)):
        raise TypeError(f"Color parameter must be a number: value={v!r}")
    v = max(v, self._lower_bound)
    v = min(v, self._upper_bound)
    g = int((v - self._lower_bound) / (self._upper_bound - self._lower_bound) * 255.0)
    for name, val in (("r", g), ("g", g), ("b", g)):
        if not isinstance(val, int):
            raise TypeError(f"Color parameter must be an int: {name}={val!r}")
        if val < 0 or val > 255:
            raise ValueError(f"Color parameter out of range: {name}={val}")
    return (g, g, g)