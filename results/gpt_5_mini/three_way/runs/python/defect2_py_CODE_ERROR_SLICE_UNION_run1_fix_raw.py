def get_paint(self, value: float) -> Tuple[int, int, int]:
    # Clamp value to bounds
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)

    # Compute normalized gray level using the clamped value
    range_span = self._upper_bound - self._lower_bound
    if range_span == 0.0:
        # Fallback to middle gray if bounds are equal (defensive)
        g = 127
    else:
        g = int((v - self._lower_bound) / range_span * 255.0)

    # Ensure g is within 0..255
    if g < 0:
        g = 0
    elif g > 255:
        g = 255

    return (g, g, g)