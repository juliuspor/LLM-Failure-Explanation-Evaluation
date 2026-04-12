def get_paint(self, value: float) -> Tuple[int, int, int]:
    # Clamp value to bounds
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)

    # Normalize to 0..1; guard against division by zero just in case
    span = self._upper_bound - self._lower_bound
    if span == 0.0:
        frac = 0.0
    else:
        frac = (v - self._lower_bound) / span

    # Convert to 0..255 using rounding, then clamp to integer range
    g = int(round(frac * 255.0))
    if g < 0:
        g = 0
    elif g > 255:
        g = 255

    return (g, g, g)