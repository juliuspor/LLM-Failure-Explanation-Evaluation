def get_paint(self, value: float) -> Tuple[int, int, int]:
    # Clamp value to bounds
    v = max(self._lower_bound, min(value, self._upper_bound))

    # Compute normalized fraction within [0,1]
    denom = (self._upper_bound - self._lower_bound)
    if denom == 0.0:
        # Should not happen because constructor forbids equal bounds, but guard anyway
        fraction = 0.0
    else:
        fraction = (v - self._lower_bound) / denom

    # Scale to 0..255 and ensure integer within bounds
    computed = round(fraction * 255.0)
    g = int(max(0, min(255, computed)))

    if g < 0 or g > 255:
        raise ValueError(f"Color parameter outside of expected range for gray channel: {g}")

    return (g, g, g)