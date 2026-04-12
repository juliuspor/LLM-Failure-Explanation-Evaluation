def get_paint(self, value: float) -> Tuple[int, int, int]:
    # Clamp value to bounds
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)

    # Safe denominator (constructor enforces lower < upper, but guard defensively)
    denom = (self._upper_bound - self._lower_bound)
    if denom == 0.0:
        raise ValueError("Invalid paint scale bounds: lower_bound and upper_bound must differ")

    # Compute gray level using the clamped value
    gray_float = (v - self._lower_bound) / denom * 255.0

    # Clamp to integer 0..255
    g = int(round(gray_float))
    if g < 0:
        g = 0
    elif g > 255:
        g = 255

    return (g, g, g)