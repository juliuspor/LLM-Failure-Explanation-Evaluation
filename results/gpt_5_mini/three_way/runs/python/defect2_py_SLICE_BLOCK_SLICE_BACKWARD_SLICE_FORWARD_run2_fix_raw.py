def get_paint(self, value: float) -> Tuple[int, int, int]:
    # Clamp value to bounds
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)

    # Ensure bounds are valid to avoid division by zero
    if self._upper_bound == self._lower_bound:
        raise ValueError(f"Invalid paint scale bounds: lower_bound ({self._lower_bound}) == upper_bound ({self._upper_bound})")

    # Compute gray level using the clamped value
    g = int((v - self._lower_bound) / (self._upper_bound - self._lower_bound) * 255.0)

    # Validate the computed component is within the expected range
    if g < 0 or g > 255:
        raise ValueError(f"Computed gray component out of range: {g} (expected 0..255) for input value {value} clamped to {v} and bounds [{self._lower_bound}, {self._upper_bound}]")

    return (g, g, g)