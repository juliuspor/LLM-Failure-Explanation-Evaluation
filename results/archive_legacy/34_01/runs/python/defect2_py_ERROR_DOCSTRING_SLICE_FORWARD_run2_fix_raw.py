def get_paint(self, value: float) -> Tuple[int, int, int]:
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)
    ratio = (v - self._lower_bound) / (self._upper_bound - self._lower_bound)
    gray_f = ratio * 255.0
    g = int(round(gray_f))
    if g < 0:
        g = 0
    if g > 255:
        g = 255
    if not (isinstance(g, int) and 0 <= g <= 255):
        raise ValueError(f"Paint produced invalid RGB: {(g, g, g)}")
    return (g, g, g)