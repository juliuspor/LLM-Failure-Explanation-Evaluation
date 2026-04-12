def get_paint(self, value: float) -> Tuple[int, int, int]:
    # Clamp value to bounds
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)

    # Defensive check: ensure denominator is non-zero (should be guaranteed by constructor)
    range_span = self._upper_bound - self._lower_bound
    if range_span == 0.0:
        raise ValueError(f"Invalid GrayPaintScale with zero span: lower_bound={self._lower_bound}, upper_bound={self._upper_bound}")

    # Use the clamped value 'v' to compute the gray component
    g = int((v - self._lower_bound) / range_span * 255.0)

    # Validate the computed component is within 0..255
    if g < 0 or g > 255:
        raise ValueError(f"Computed gray component out of range: g={g} (from value={value}, clamped to {v}, bounds=[{self._lower_bound}, {self._upper_bound}])")

    return (g, g, g)