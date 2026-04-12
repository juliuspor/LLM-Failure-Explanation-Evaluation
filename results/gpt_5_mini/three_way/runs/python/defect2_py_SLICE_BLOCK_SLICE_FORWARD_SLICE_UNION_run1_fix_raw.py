def get_paint(self, value: float) -> Tuple[int, int, int]:
    # Ensure bounds are valid to avoid division by zero
    if self._upper_bound <= self._lower_bound:
        raise ValueError("Invalid bounds: lower_bound must be less than upper_bound")

    # Clamp value to bounds
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)

    # Normalize clamped value to [0.0, 1.0] and scale to 0..255
    ratio = (v - self._lower_bound) / (self._upper_bound - self._lower_bound)
    g = int(ratio * 255.0)

    # Ensure g is within valid range (safety for rounding)
    if g < 0:
        g = 0
    elif g > 255:
        g = 255

    return (g, g, g)