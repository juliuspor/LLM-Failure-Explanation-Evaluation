def get_paint(self, value: float) -> Tuple[int, int, int]:
    # Clamp value to bounds
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)

    # Compute grayscale using the clamped value
    g = int((v - self._lower_bound) / (self._upper_bound - self._lower_bound) * 255.0)

    # Clamp g to valid range 0..255
    if g < 0:
        g = 0
    elif g > 255:
        g = 255

    return (g, g, g)