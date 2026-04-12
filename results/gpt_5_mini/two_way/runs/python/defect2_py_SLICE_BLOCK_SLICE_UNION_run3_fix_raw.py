def get_paint(self, value: float) -> Tuple[int, int, int]:
    # Clamp value to bounds
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)

    # Avoid division by zero by using bounds validated in __init__ (but be defensive)
    span = (self._upper_bound - self._lower_bound)
    if span == 0.0:
        # fallback to middle gray
        g = 127
    else:
        g = int(round((v - self._lower_bound) / span * 255.0))

    # Validate range and provide informative message
    if g < 0 or g > 255:
        raise ValueError(f"Color parameter outside of expected range: g={g}")

    return (g, g, g)