def get_paint(self, value: float) -> Tuple[int, int, int]:
    if self._upper_bound == self._lower_bound:
        raise ValueError(f"Invalid bounds: lower_bound ({self._lower_bound}) == upper_bound ({self._upper_bound})")
    if value < self._lower_bound or value > self._upper_bound:
        raise ValueError(f"value {value} out of bounds [{self._lower_bound}, {self._upper_bound}]")
    ratio = (value - self._lower_bound) / (self._upper_bound - self._lower_bound)
    g = int(ratio * 255.0)
    if g < 0 or g > 255:
        raise ValueError(f"Computed gray channel out of range: g={g} from value={value}")
    return (g, g, g)