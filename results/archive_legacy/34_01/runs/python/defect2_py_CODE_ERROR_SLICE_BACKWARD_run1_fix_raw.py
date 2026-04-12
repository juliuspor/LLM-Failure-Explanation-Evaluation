def get_paint(self, value: float) -> Tuple[int, int, int]:
    v = max(min(value, self._upper_bound), self._lower_bound)
    if self._upper_bound == self._lower_bound:
        g = 0
    else:
        g = int((v - self._lower_bound) / (self._upper_bound - self._lower_bound) * 255.0)
    if g < 0 or g > 255:
        raise ValueError(f"Color parameter out of range: g={g}, value={value}, bounds=({self._lower_bound},{self._upper_bound})")
    return (g, g, g)