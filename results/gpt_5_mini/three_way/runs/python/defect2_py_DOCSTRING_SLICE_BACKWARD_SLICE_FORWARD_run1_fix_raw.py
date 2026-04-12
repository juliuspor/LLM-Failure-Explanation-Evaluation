def get_paint(self, value: float) -> Tuple[int, int, int]:
    # Clamp value to bounds
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)

    # Guard against zero division (shouldn't happen because constructor enforces lower<upper)
    span = (self._upper_bound - self._lower_bound)
    if span == 0.0:
        raise ValueError("Scale bounds must differ (upper_bound != lower_bound)")

    # Compute gray component from the clamped value
    g = int((v - self._lower_bound) / span * 255.0)

    # Validate range
    if g < 0 or g > 255:
        raise ValueError(f"Computed color component out of range 0..255: g={g}")

    return (g, g, g)