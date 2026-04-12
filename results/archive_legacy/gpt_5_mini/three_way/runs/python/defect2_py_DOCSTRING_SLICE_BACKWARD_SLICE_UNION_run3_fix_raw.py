def get_paint(self, value: float) -> Tuple[int, int, int]:
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)
    if self._upper_bound == self._lower_bound:
        raise ValueError(f"Invalid bounds in get_paint: lower_bound={self._lower_bound}, upper_bound={self._upper_bound}")
    fraction = (v - self._lower_bound) / (self._upper_bound - self._lower_bound)
    intensity = int(round(fraction * 255.0))
    if intensity < 0:
        intensity = 0
    elif intensity > 255:
        intensity = 255
    return (intensity, intensity, intensity)