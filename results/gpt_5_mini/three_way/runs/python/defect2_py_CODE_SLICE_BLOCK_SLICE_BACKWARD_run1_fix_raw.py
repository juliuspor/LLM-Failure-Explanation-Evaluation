def get_paint(self, value: float) -> Tuple[int, int, int]:
    # Clamp value to bounds
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)

    # Defensive check to avoid division by zero (constructor should prevent this)
    span = (self._upper_bound - self._lower_bound)
    if span == 0.0:
        raise ValueError("Upper and lower bounds must not be equal.")

    g = int((v - self._lower_bound) / span * 255.0)

    # Clamp g to valid range just in case of rounding
    if g < 0:
        g = 0
    elif g > 255:
        g = 255

    # In Python, we validate the range (Java Color constructor does this)
    if g < 0 or g > 255:
        raise ValueError(f"Color parameter outside of expected range: Red Green Blue")

    return (g, g, g)