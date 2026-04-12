def get_paint(self, value: float) -> Tuple[int, int, int]:
    # Clamp value to bounds
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)

    # Compute normalized position in range (safe because __init__ forbids equal bounds)
    normalized = (v - self._lower_bound) / (self._upper_bound - self._lower_bound)

    # Convert to 0..255 using rounding to be symmetric
    g = int(round(normalized * 255.0))

    # Validate range
    if g < 0 or g > 255:
        raise ValueError(f"Computed gray component out of range: g={g}")

    return (g, g, g)