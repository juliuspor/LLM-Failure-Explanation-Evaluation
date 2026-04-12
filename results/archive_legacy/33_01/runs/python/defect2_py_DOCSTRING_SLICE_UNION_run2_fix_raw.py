def get_paint(self, value: float) -> Tuple[int, int, int]:
    if self._upper_bound == self._lower_bound:
        raise ValueError(f"Invalid bounds: upper_bound ({self._upper_bound}) equals lower_bound ({self._lower_bound})")
    norm = (value - self._lower_bound) / (self._upper_bound - self._lower_bound)
    if norm < 0.0:
        norm = 0.0
    elif norm > 1.0:
        norm = 1.0
    g = int(round(norm * 255.0))
    if g < 0 or g > 255:
        raise ValueError(f"Computed color component out of range: g={g}, value={value}, bounds=({self._lower_bound},{self._upper_bound})")
    return (g, g, g)