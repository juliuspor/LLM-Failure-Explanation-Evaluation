def get_paint(self, value: float) -> Tuple[int, int, int]:
    # Clamp value to bounds
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)

    # Avoid division by zero if bounds are equal (shouldn't happen due to constructor,
    # but guard defensively)
    range_span = self._upper_bound - self._lower_bound
    if range_span == 0.0:
        g = 0
    else:
        # Use the clamped value 'v' and round to nearest integer
        g = int(round((v - self._lower_bound) / range_span * 255.0))

    # Validate range
    if g < 0 or g > 255:
        raise ValueError(f"Color parameter outside of expected range: Red Green Blue")

    return (g, g, g)