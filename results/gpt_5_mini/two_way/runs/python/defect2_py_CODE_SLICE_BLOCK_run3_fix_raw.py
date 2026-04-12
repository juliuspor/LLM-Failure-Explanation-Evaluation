def get_paint(self, value: float) -> Tuple[int, int, int]:
    # Clamp value to bounds
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)

    # Defensive: avoid division by zero though constructor should prevent equal bounds
    span = (self._upper_bound - self._lower_bound)
    if span == 0.0:
        g = 0
    else:
        g = int((v - self._lower_bound) / span * 255.0)

    # Validate the range
    if g < 0 or g > 255:
        raise ValueError(f"Color parameter outside of expected range: {g}")

    return (g, g, g)