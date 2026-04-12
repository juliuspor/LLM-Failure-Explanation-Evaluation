def get_paint(self, value: float) -> Tuple[int, int, int]:
    try:
        v_in = float(value)
    except Exception:
        raise ValueError(f"Value must be numeric: {value}")
    v = max(v_in, self._lower_bound)
    v = min(v, self._upper_bound)
    denom = self._upper_bound - self._lower_bound
    if denom == 0.0:
        g = 127
    else:
        ratio = (v - self._lower_bound) / denom
        g = int(round(ratio * 255.0))
    if g < 0 or g > 255:
        raise ValueError(f"Color parameter outside of expected range: g={g}")
    return (g, g, g)