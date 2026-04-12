def get_paint(self, value: float) -> Tuple[int, int, int]:
    # Clamp value to bounds
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)

    # Avoid division by zero (constructor should prevent this, but be defensive)
    denom = (self._upper_bound - self._lower_bound)
    if denom == 0.0:
        # If bounds are the same, treat as middle gray
        g = 127
    else:
        # Use the clamped value 'v' for calculation
        g = int(round((v - self._lower_bound) / denom * 255.0))

    # Ensure g is within 0..255
    if g < 0:
        g = 0
    elif g > 255:
        g = 255

    return (g, g, g)