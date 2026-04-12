def get_paint(self, value: float) -> Tuple[int, int, int]:
    # Clamp value to bounds
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)

    # Protect against accidental zero-range (shouldn't happen due to constructor,
    # but guard against it to avoid ZeroDivisionError)
    span = self._upper_bound - self._lower_bound
    if span == 0.0:
        raise ValueError("Invalid GrayPaintScale: lower_bound and upper_bound are equal")

    # Compute gray level based on the clamped value
    g = int((v - self._lower_bound) / span * 255.0)

    # Validate component range explicitly and provide informative message
    if g < 0 or g > 255:
        raise ValueError(f"Color parameter outside of expected range: r={g}, g={g}, b={g}")

    return (g, g, g)