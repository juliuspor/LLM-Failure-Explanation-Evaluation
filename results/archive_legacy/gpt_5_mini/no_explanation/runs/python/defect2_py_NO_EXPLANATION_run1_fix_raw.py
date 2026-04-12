def get_paint(self, value: float) -> Tuple[int, int, int]:
    # Clamp value to bounds
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)

    # Compute normalized position in range [0.0, 1.0]
    span = self._upper_bound - self._lower_bound
    if span == 0.0:
        norm = 0.0
    else:
        norm = (v - self._lower_bound) / span

    # Map to 0-255 and convert to int with rounding
    g = int(round(norm * 255.0))

    # Ensure within bounds [0, 255]
    if g < 0:
        g = 0
    elif g > 255:
        g = 255

    return (g, g, g)