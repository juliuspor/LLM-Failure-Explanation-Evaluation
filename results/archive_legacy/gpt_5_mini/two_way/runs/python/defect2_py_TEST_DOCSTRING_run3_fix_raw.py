def get_paint(self, value: float) -> Tuple[int, int, int]:
    v = max(min(value, self._upper_bound), self._lower_bound)
    denom = (self._upper_bound - self._lower_bound)
    if denom == 0.0:
        raise ValueError("upper_bound and lower_bound must differ")
    intensity = (v - self._lower_bound) / denom * 255.0
    if intensity < 0.0:
        intensity = 0.0
    elif intensity > 255.0:
        intensity = 255.0
    i = int(intensity)
    return (i, i, i)