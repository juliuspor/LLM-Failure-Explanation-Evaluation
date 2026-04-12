def get_paint(self, value: float) -> Tuple[int, int, int]:
    # Clamp value to bounds
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)

    # Normalize clamped value to a 0..1 range and scale to 0..255
    # Division by zero is prevented by constructor validation (lower < upper)
    fraction = (v - self._lower_bound) / (self._upper_bound - self._lower_bound)
    g = int(round(fraction * 255.0))

    # Ensure the resulting component is within valid 0..255 range
    g = max(0, min(255, g))

    return (g, g, g)