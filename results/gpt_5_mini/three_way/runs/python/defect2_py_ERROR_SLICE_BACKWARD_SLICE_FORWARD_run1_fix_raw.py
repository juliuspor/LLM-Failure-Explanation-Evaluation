def get_paint(self, value: float) -> Tuple[int, int, int]:
    # Clamp value to bounds
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)

    # Normalize using the clamped value so the result is within 0..255
    g = int((v - self._lower_bound) / (self._upper_bound - self._lower_bound) * 255.0)

    # Validate the computed component is within the expected range
    if g < 0 or g > 255:
        raise ValueError(f"Computed gray component {g} outside of expected range 0..255")

    return (g, g, g)