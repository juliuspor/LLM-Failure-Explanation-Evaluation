def get_paint(self, value: float) -> Tuple[int, int, int]:
    if value is None:
        raise ValueError("Value must be a number")
    try:
        v = float(value)
    except (TypeError, ValueError):
        raise ValueError("Value must be a number")
    if v != v or v == float('inf') or v == float('-inf'):
        raise ValueError("Value must be a finite number")
    v = max(v, self._lower_bound)
    v = min(v, self._upper_bound)
    span = self._upper_bound - self._lower_bound
    if span == 0:
        fraction = 0.0
    else:
        fraction = (v - self._lower_bound) / span
    g = int(round(fraction * 255.0))
    if g < 0:
        g = 0
    elif g > 255:
        g = 255
    return (g, g, g)