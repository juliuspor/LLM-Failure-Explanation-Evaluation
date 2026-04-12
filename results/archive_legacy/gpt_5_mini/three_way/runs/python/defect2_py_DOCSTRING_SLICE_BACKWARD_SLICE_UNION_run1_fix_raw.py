def get_paint(self, value: float) -> Tuple[int, int, int]:
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)
    denom = (self._upper_bound - self._lower_bound)
    if denom == 0.0:
        raise ValueError(f"Invalid bounds: lower_bound ({self._lower_bound}) must be less than upper_bound ({self._upper_bound})")
    ratio = (v - self._lower_bound) / denom
    gray = int(round(ratio * 255.0))
    if gray < 0:
        gray = 0
    elif gray > 255:
        gray = 255
    return (gray, gray, gray)