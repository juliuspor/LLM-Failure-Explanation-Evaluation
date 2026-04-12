def get_paint(self, value: float) -> Tuple[int, int, int]:
    # Clamp value to bounds
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)

    # Compute grayscale component using the clamped value
    g = int((v - self._lower_bound) / (self._upper_bound - self._lower_bound) * 255.0)

    # Ensure component is within 0..255 (defensive clamping)
    if g < 0:
        g = 0
    elif g > 255:
        g = 255

    # Final validation (should not fail after clamping, but kept for explicit error if something unexpected occurs)
    if g < 0 or g > 255:
        raise ValueError(f"Gray component out of range: {g}")

    return (g, g, g)