def get_paint(self, value: float) -> Tuple[int, int, int]:
    # Clamp value to bounds
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)

    # Defensive: avoid division by zero (constructor should prevent equal bounds)
    span = (self._upper_bound - self._lower_bound)
    if span == 0.0:
        # fallback to middle gray
        g = 127
    else:
        # compute gray using the clamped value
        g = int((v - self._lower_bound) / span * 255.0)

    # Clamp to valid byte range to account for floating point imprecision
    if g < 0:
        g = 0
    elif g > 255:
        g = 255

    return (g, g, g)