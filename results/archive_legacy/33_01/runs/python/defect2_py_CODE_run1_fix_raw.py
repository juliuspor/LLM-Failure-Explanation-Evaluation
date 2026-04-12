def get_paint(self, value: float) -> Tuple[int, int, int]:
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)
    if self._upper_bound == self._lower_bound:
        raise ValueError("upper_bound equals lower_bound; cannot scale value")
    g = int((v - self._lower_bound) / (self._upper_bound - self._lower_bound) * 255.0)
    if g < 0 or g > 255:
        raise ValueError(f"Computed g={g} outside 0..255 for value={value}, clamped v={v}, bounds=({self._lower_bound},{self._upper_bound})")
    return (g, g, g)