def get_paint(self, value: float) -> Tuple[int, int, int]:
    # Clamp value to bounds
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)

    # Compute grayscale using the clamped value (avoid using the original value)
    # __init__ enforces upper > lower, so denominator should not be zero.
    ratio = (v - self._lower_bound) / (self._upper_bound - self._lower_bound)
    g = int(round(ratio * 255.0))

    # Clamp final component to 0..255
    if g < 0:
        g = 0
    elif g > 255:
        g = 255

    # Final sanity check (should not trigger)
    if g < 0 or g > 255:
        raise ValueError(f"Color parameter outside of expected range for grayscale component: g={g}")

    return (g, g, g)