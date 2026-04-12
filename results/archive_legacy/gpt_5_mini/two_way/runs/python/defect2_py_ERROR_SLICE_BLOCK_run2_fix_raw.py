def get_paint(self, value: float) -> Tuple[int, int, int]:
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)
    g = int((v - self._lower_bound) / (self._upper_bound - self._lower_bound) * 255.0)
    def _validate(name: str, val: int):
        if val < 0 or val > 255:
            raise ValueError(f"Color parameter '{name}' out of range: {val} (expected 0..255)")
    _validate('r', g)
    _validate('g', g)
    _validate('b', g)
    return (g, g, g)