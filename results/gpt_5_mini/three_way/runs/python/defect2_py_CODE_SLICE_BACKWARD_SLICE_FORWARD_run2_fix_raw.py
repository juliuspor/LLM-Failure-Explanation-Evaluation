def get_paint(self, value: float) -> Tuple[int, int, int]:
    # Clamp value to bounds
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)

    # compute normalized fraction using clamped value
    denom = (self._upper_bound - self._lower_bound)
    if denom == 0.0:
        # defensive: should not happen because constructor enforces bounds
        fraction = 0.0
    else:
        fraction = (v - self._lower_bound) / denom

    g = int(fraction * 255.0)

    # In Python, we validate the range (Java Color constructor does this)
    if g < 0 or g > 255:
        raise ValueError(f"Color parameter outside of expected range: Red Green Blue")

    return (g, g, g)