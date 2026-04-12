def get_paint(self, value: float) -> Tuple[int, int, int]:
    # Clamp value to bounds
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)

    # Prevent division by zero if bounds are equal (shouldn't happen due to ctor,
    # but guard defensively)
    span = self._upper_bound - self._lower_bound
    if span == 0.0:
        raise ValueError(f"Invalid scale bounds: lower_bound ({self._lower_bound}) == upper_bound ({self._upper_bound})")

    gray = int(round((v - self._lower_bound) / span * 255.0))

    if gray < 0 or gray > 255:
        raise ValueError(f"Computed gray value out of range: gray={gray} (expected 0..255)")

    return (gray, gray, gray)