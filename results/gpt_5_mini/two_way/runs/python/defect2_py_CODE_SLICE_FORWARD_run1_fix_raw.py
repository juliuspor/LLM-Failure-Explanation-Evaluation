def get_paint(self, value: float) -> Tuple[int, int, int]:
    # Clamp value to bounds
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)

    # Avoid division by zero (shouldn't happen because constructor enforces lower<upper)
    span = self._upper_bound - self._lower_bound
    if span == 0.0:
        g = 0
    else:
        g = int((v - self._lower_bound) / span * 255.0)

    # Clamp g to valid RGB range
    g = max(0, min(255, g))

    return (g, g, g)