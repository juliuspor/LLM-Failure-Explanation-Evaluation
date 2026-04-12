def get_paint(self, value: float) -> Tuple[int, int, int]:
    v = value
    if v < self._lower_bound:
        v = self._lower_bound
    if v > self._upper_bound:
        v = self._upper_bound
    denom = (self._upper_bound - self._lower_bound)
    if denom == 0:
        proportion = 0.0
    else:
        proportion = (v - self._lower_bound) / denom
    if proportion < 0.0:
        proportion = 0.0
    if proportion > 1.0:
        proportion = 1.0
    g = int(proportion * 255.0)
    if g < 0:
        g = 0
    if g > 255:
        g = 255
    return (g, g, g)