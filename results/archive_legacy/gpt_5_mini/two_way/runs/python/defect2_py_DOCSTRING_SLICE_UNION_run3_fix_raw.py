def get_paint(self, value: float) -> Tuple[int, int, int]:
    if self._upper_bound == self._lower_bound:
        raise ValueError(f"Invalid bounds: lower_bound ({self._lower_bound}) == upper_bound ({self._upper_bound})")
    v = max(self._lower_bound, min(value, self._upper_bound))
    ratio = (v - self._lower_bound) / (self._upper_bound - self._lower_bound)
    level = int(ratio * 255.0)
    if level < 0:
        level = 0
    elif level > 255:
        level = 255
    return (level, level, level)