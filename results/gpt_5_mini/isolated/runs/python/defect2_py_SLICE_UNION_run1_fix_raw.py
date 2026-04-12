def get_paint(self, value: float) -> Tuple[int, int, int]:
    # Clamp value to bounds
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)

    # Protect against zero division (shouldn't occur because __init__ enforces lower < upper)
    span = self._upper_bound - self._lower_bound
    if span == 0.0:
        raise ValueError("Invalid paint scale bounds: upper_bound must be greater than lower_bound")

    # Compute a single gray component based on the clamped value
    g = int(round((v - self._lower_bound) / span * 255.0))

    # Validate component range
    if g < 0 or g > 255:
        raise ValueError(f"Color component out of range: g={g}")

    return (g, g, g)