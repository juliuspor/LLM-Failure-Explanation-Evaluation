def get_paint(self, value: float) -> Tuple[int, int, int]:
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)
    fraction = (v - self._lower_bound) / (self._upper_bound - self._lower_bound)
    intensity = int(round(fraction * 255.0))
    intensity = max(0, min(255, intensity))
    return (intensity, intensity, intensity)