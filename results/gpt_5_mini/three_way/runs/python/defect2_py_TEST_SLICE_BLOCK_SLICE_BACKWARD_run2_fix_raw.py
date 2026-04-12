def get_paint(self, value: float) -> Tuple[int, int, int]:
    # Clamp value to bounds
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)

    # Defensive: avoid division by zero, though constructor enforces lower < upper
    span = (self._upper_bound - self._lower_bound)
    if span == 0.0:
        g = 0
    else:
        # Use the clamped value 'v' for normalization, then clamp the resulting component to 0..255
        normalized = (v - self._lower_bound) / span
        g = int(normalized * 255.0)
        if g < 0:
            g = 0
        elif g > 255:
            g = 255

    return (g, g, g)