def get_paint(self, value: float) -> Tuple[int, int, int]:
    # Clamp value to bounds
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)

    lower = self._lower_bound
    upper = self._upper_bound
    span = upper - lower

    # If span is zero (shouldn't happen because constructor forbids it),
    # return a mid-gray value to avoid division by zero.
    if span == 0.0:
        g = 128
        return (g, g, g)

    # Normalize and clamp to [0.0, 1.0]
    t = (v - lower) / span
    if t < 0.0:
        t = 0.0
    elif t > 1.0:
        t = 1.0

    g = int(t * 255.0)

    # Ensure within valid range (defensive)
    if g < 0 or g > 255:
        raise ValueError(f"Computed grayscale value {g} out of range 0..255 for input {value} with bounds ({lower},{upper})")

    return (g, g, g)