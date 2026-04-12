def get_paint(self, value: float) -> Tuple[int, int, int]:
    # Clamp value to bounds
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)

    # compute gray based on the clamped value
    g = int((v - self._lower_bound) / (self._upper_bound - self._lower_bound) * 255.0)

    # Validate range
    if g < 0 or g > 255:
        raise ValueError(f"Color parameter outside of expected range: r={g}, g={g}, b={g}")

    return (g, g, g)