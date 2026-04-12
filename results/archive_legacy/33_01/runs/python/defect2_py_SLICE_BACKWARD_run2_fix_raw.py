def get_paint(self, value: float) -> Tuple[int, int, int]:
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)
    denom = (self._upper_bound - self._lower_bound)
    if denom == 0.0:
        raise ValueError(f"get_paint: upper_bound ({self._upper_bound}) equals lower_bound ({self._lower_bound}); cannot compute gray level")
    g = int((v - self._lower_bound) / denom * 255.0)
    if g < 0 or g > 255:
        raise ValueError(f"get_paint: computed gray value {g} outside 0..255 for input value={value}, bounds=({self._lower_bound},{self._upper_bound})")
    return (g, g, g)