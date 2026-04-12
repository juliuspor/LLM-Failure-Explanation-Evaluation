def get_paint(self, value: float) -> Tuple[int, int, int]:
    # Clamp value to bounds
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)

    # If original value was outside bounds, signal that (clear message)
    if value < self._lower_bound or value > self._upper_bound:
        raise ValueError(f"Value {value} outside range [{self._lower_bound}, {self._upper_bound}]")

    # Compute normalized gray level using the clamped value (denominator guaranteed > 0 by constructor)
    ratio = (v - self._lower_bound) / (self._upper_bound - self._lower_bound)
    g = int(ratio * 255.0)

    # Clamp g to valid byte range to guard against rounding issues
    if g < 0:
        g = 0
    elif g > 255:
        g = 255

    return (g, g, g)