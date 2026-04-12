def get_paint(self, value: float) -> Tuple[int, int, int]:
    if self._upper_bound == self._lower_bound:
        raise ValueError(f"upper_bound ({self._upper_bound}) equals lower_bound ({self._lower_bound}); cannot normalize value")
    if value < self._lower_bound or value > self._upper_bound:
        raise ValueError(f"value {value} is outside configured bounds [{self._lower_bound}, {self._upper_bound}]")
    normalized = (value - self._lower_bound) / (self._upper_bound - self._lower_bound)
    g = int(normalized * 255.0)
    if g < 0 or g > 255:
        raise ValueError(f"Computed channel g={g} out of range 0..255 for value={value}, bounds=[{self._lower_bound},{self._upper_bound}]")
    return (g, g, g)