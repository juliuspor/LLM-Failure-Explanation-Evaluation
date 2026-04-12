def get_paint(self, value: float) -> Tuple[int, int, int]:
    # Clamp value to bounds
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)

    # Normalize to 0..1 and scale to 0..255
    if self._upper_bound == self._lower_bound:
        # Shouldn't happen due to constructor, but guard against division by zero
        normalized = 0.0
    else:
        normalized = (v - self._lower_bound) / (self._upper_bound - self._lower_bound)

    g = int(round(normalized * 255.0))

    # Ensure within 0..255
    if g < 0:
        g = 0
    elif g > 255:
        g = 255

    return (g, g, g)