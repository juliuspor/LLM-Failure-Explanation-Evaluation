def get_paint(self, value: float) -> Tuple[int, int, int]:
    # Clamp value to bounds
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)

    range_width = self._upper_bound - self._lower_bound
    if range_width == 0.0:
        # Defensive: avoid division by zero
        raise ValueError("Invalid scale bounds: lower and upper bounds must differ.")

    g = int((v - self._lower_bound) / range_width * 255.0)

    # In Python, we validate the range (Java Color constructor does this)
    if g < 0 or g > 255:
        raise ValueError("Color parameter outside of expected range: Red Green Blue")

    return (g, g, g)