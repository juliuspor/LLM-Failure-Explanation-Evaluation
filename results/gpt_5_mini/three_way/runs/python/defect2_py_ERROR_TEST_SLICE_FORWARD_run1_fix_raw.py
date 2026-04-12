def get_paint(self, value: float) -> Tuple[int, int, int]:
    # Clamp value to bounds
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)

    # Avoid division by zero (constructor already prevents equal bounds)
    span = self._upper_bound - self._lower_bound
    if span == 0:
        raise ValueError("Invalid scale with zero span")

    # Compute normalized value in [0.0, 1.0]
    normalized = (v - self._lower_bound) / span

    # Convert to 0..255 and ensure integer within bounds
    g = int(normalized * 255.0)
    g = max(0, min(255, g))

    return (g, g, g)
