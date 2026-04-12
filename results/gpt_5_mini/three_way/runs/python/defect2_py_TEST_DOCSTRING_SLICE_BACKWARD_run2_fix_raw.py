def get_paint(self, value: float) -> Tuple[int, int, int]:
    # Clamp value to bounds
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)

    # Guard against degenerate range (shouldn't happen because constructor forbids it)
    range_span = self._upper_bound - self._lower_bound
    if range_span == 0.0:
        fraction = 0.0
    else:
        fraction = (v - self._lower_bound) / range_span

    # Convert to 0..255, using rounding to be close to Java's behavior
    g = int(round(fraction * 255.0))

    # Ensure within bounds; this should always be true due to clamping
    if g < 0 or g > 255:
        raise ValueError(f"Computed gray component out of range: {g}")

    return (g, g, g)