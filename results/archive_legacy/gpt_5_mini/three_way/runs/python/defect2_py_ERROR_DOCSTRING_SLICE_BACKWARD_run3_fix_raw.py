def get_paint(self, value: float) -> Tuple[int, int, int]:
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)
    denom = (self._upper_bound - self._lower_bound)
    if denom == 0:
        raise ValueError(f"Invalid bounds: lower_bound == upper_bound == {self._lower_bound}")
    intensity = int((v - self._lower_bound) / denom * 255.0)
    if intensity < 0 or intensity > 255:
        raise ValueError(f"Color parameter outside 0..255: intensity={intensity} for value={value} bounds=({self._lower_bound},{self._upper_bound})")
    return (intensity, intensity, intensity)