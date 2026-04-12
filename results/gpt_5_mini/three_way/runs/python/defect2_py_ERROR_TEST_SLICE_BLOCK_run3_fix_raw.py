def get_paint(self, value: float) -> Tuple[int, int, int]:
    # Clamp value to bounds
    v = max(self._lower_bound, min(self._upper_bound, value))

    # Normalize to [0.0, 1.0]
    fraction = (v - self._lower_bound) / (self._upper_bound - self._lower_bound)

    # Compute gray component and ensure an integer in 0..255
    g = int(round(fraction * 255.0))
    if g < 0:
        g = 0
    elif g > 255:
        g = 255

    # Sanity check (should not trigger)
    if g < 0 or g > 255:
        raise ValueError(f"Color component out of range: {g}")

    return (g, g, g)