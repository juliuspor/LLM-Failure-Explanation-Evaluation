def get_paint(self, value: float) -> Tuple[int, int, int]:
    # Clamp value to bounds
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)

    # Prevent division by zero if bounds are equal
    range_span = self._upper_bound - self._lower_bound
    if range_span == 0.0:
        raise ValueError("Invalid paint scale: lower_bound and upper_bound are equal")

    g = int((v - self._lower_bound) / range_span * 255.0)

    # In Python, we validate the range (Java Color constructor does this)
    if g < 0 or g > 255:
        raise ValueError(f"Color parameter outside of expected range: {g}")

    return (g, g, g)