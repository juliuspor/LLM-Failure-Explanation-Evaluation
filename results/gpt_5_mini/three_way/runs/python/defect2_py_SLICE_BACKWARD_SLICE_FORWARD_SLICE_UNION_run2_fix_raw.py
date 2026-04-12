def get_paint(self, value: float) -> Tuple[int, int, int]:
    # Clamp value to bounds
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)

    denom = (self._upper_bound - self._lower_bound)
    if denom == 0.0:
        # Should not happen because __init__ prevents this, but guard defensively
        g = 0
    else:
        # Use the clamped value v for the interpolation
        g = int((v - self._lower_bound) / denom * 255.0)

    # Ensure g is within 0..255 after rounding
    if g < 0 or g > 255:
        raise ValueError(f"Computed gray level {g} out of range 0..255 for value {value} with bounds [{self._lower_bound}, {self._upper_bound}]")

    return (g, g, g)