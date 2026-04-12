def get_paint(self, value: float) -> Tuple[int, int, int]:
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)
    span = self._upper_bound - self._lower_bound
    if span == 0.0:
        raise ValueError(f"Invalid bounds: lower_bound ({self._lower_bound}) == upper_bound ({self._upper_bound})")
    ratio = (v - self._lower_bound) / span
    ratio = max(0.0, min(1.0, ratio))
    g = int(ratio * 255.0)
    if g < 0 or g > 255:
        raise ValueError(f"computed gray {g} from value {value} outside 0..255 for bounds [{self._lower_bound}, {self._upper_bound}]")
    return (g, g, g)