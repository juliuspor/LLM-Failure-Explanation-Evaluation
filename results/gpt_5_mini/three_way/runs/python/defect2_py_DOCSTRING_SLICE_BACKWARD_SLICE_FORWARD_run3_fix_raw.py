def get_paint(self, value: float) -> Tuple[int, int, int]:
    # Clamp value to bounds
    v = max(min(value, self._upper_bound), self._lower_bound)

    # Compute gray level using the clamped value to avoid out-of-range results
    span = self._upper_bound - self._lower_bound
    if span == 0.0:
        # Defensive: should not happen because __init__ prevents equal bounds
        raise ValueError(f"Invalid scale with zero range: lower_bound={self._lower_bound}, upper_bound={self._upper_bound}")

    g = int((v - self._lower_bound) / span * 255.0)

    # Validate the computed component
    if g < 0 or g > 255:
        raise ValueError(f"Computed gray component out of range: {g} (expected 0..255) for value={value} clamped to {v} with bounds [{self._lower_bound}, {self._upper_bound}]")

    return (g, g, g)