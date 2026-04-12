def get_paint(self, value: float) -> Tuple[int, int, int]:
    # Clamp value to bounds first
    try:
        v = float(value)
    except (TypeError, ValueError):
        raise ValueError(f"Invalid numeric value: {value}")

    if v != v:  # NaN
        raise ValueError(f"Invalid numeric value: {value}")

    # Clamp to the configured bounds
    v = max(v, self._lower_bound)
    v = min(v, self._upper_bound)

    # Guard against zero range (shouldn't happen because constructor checks bounds)
    span = (self._upper_bound - self._lower_bound)
    if span == 0:
        # Fall back to mid-gray
        normalized = 0.5
    else:
        normalized = (v - self._lower_bound) / span

    # Clamp normalized to [0.0, 1.0] to avoid NaN/inf or out-of-range values
    if normalized != normalized:  # NaN
        raise ValueError(f"Invalid numeric computation for value: {value}")
    normalized = max(0.0, min(1.0, normalized))

    g = int(round(normalized * 255.0))

    # Validate range
    if g < 0 or g > 255:
        raise ValueError(f"Color parameter outside of expected range: {g} {g} {g}")

    return (g, g, g)