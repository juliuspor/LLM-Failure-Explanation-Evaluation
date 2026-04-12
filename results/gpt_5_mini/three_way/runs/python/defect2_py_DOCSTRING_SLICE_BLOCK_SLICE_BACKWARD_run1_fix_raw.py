def get_paint(self, value: float) -> Tuple[int, int, int]:
    # Clamp value to bounds
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)

    span = self._upper_bound - self._lower_bound
    if span == 0.0:
        raise ValueError("Upper and lower bounds must not be equal.")

    # Compute a single gray component from the clamped value
    g = int((v - self._lower_bound) / span * 255.0)

    # Validate all components (they are the same here)
    if g < 0 or g > 255:
        raise ValueError("Color parameter outside of expected range: Red Green Blue")

    return (g, g, g)