def get_paint(self, value: float) -> Tuple[int, int, int]:
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)
    span = self._upper_bound - self._lower_bound
    if span == 0:
        return (128, 128, 128)
    g = int((v - self._lower_bound) / span * 255.0)
    if g < 0 or g > 255:
        raise ValueError(f"Computed grayscale {g} is outside 0-255 for value={value}, bounds=({self._lower_bound},{self._upper_bound})")
    return (g, g, g)