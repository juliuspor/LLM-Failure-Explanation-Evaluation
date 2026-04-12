def get_paint(self, value: float) -> Tuple[int, int, int]:
    if self._upper_bound == self._lower_bound:
        raise ValueError(f"Invalid bounds: lower={self._lower_bound}, upper={self._upper_bound}")
    v_clamped = max(value, self._lower_bound)
    v_clamped = min(v_clamped, self._upper_bound)
    fraction = (v_clamped - self._lower_bound) / (self._upper_bound - self._lower_bound)
    gray = int(round(fraction * 255.0))
    if gray < 0 or gray > 255:
        raise ValueError(f"Computed color component out of range: value={value}, component_value={gray}, bounds=({self._lower_bound},{self._upper_bound})")
    return (gray, gray, gray)