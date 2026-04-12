def get_paint(self, value: float) -> Tuple[int, int, int]:
    # Clamp input value to bounds
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)

    # Compute normalized fraction in [0.0, 1.0]
    span = self._upper_bound - self._lower_bound
    fraction = (v - self._lower_bound) / span if span != 0.0 else 0.0
    # Guard against any floating point overshoot
    if fraction < 0.0:
        fraction = 0.0
    elif fraction > 1.0:
        fraction = 1.0

    # Map to 0..255 using truncation toward zero, matching Java's behavior
    g = int(fraction * 255.0)

    # Final safety clamp to ensure within valid byte range
    if g < 0:
        g = 0
    elif g > 255:
        g = 255

    return (g, g, g)