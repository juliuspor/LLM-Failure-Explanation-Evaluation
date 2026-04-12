def get_paint(self, value: float) -> Tuple[int, int, int]:
    # Clamp value to bounds
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)

    # Defensive: avoid division by zero (shouldn't happen due to constructor)
    span = self._upper_bound - self._lower_bound
    if span == 0.0:
        scale = 0.0
    else:
        scale = (v - self._lower_bound) / span

    # Compute gray component, round to nearest and clamp to 0..255
    g = int(round(scale * 255.0))
    if g < 0:
        g = 0
    elif g > 255:
        g = 255

    return (g, g, g)