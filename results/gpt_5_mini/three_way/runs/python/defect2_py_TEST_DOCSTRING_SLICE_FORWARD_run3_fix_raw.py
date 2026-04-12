def get_paint(self, value: float) -> Tuple[int, int, int]:
    # Clamp value to bounds
    v = max(self._lower_bound, min(self._upper_bound, value))

    # Avoid division by zero; if bounds are equal (shouldn't happen due to ctor), treat position as 0.0
    span = self._upper_bound - self._lower_bound
    if span == 0.0:
        position = 0.0
    else:
        position = (v - self._lower_bound) / span

    # Compute component with rounding, then clamp to 0..255 to guard against floating point issues
    g = int(round(position * 255.0))
    g = max(0, min(255, g))

    return (g, g, g)