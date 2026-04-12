def get_paint(self, value: float) -> Tuple[int, int, int]:
    # Clamp value to bounds
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)

    # Compute normalized fraction using clamped v to avoid issues and ensure consistent results
    denom = (self._upper_bound - self._lower_bound)
    if denom == 0.0:
        # Defensive: if bounds were equal (should be prevented by constructor), treat as middle gray
        g = 128
    else:
        frac = (v - self._lower_bound) / denom
        g = int(frac * 255.0)

    # Clamp g to valid byte range
    if g < 0:
        g = 0
    elif g > 255:
        g = 255

    # Validate and provide helpful error if something unexpected occurred
    if g < 0 or g > 255:
        raise ValueError(f"Color parameter outside of expected range: g={g}, value={value}")

    return (g, g, g)