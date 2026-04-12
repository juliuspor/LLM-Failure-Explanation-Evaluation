def get_paint(self, value: float) -> Tuple[int, int, int]:
    """Returns an RGB color tuple for the specified value.

    Args:
        value: the value

    Returns:
        A tuple (r, g, b) representing the grayscale color

    Raises:
        ValueError: If the computed channel value is outside 0-255 range
    """
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)
    g = int((v - self._lower_bound) / (self._upper_bound - self._lower_bound) * 255.0)
    if g < 0 or g > 255:
        raise ValueError(f"Color parameter out of range: g={g} (expected 0-255)")
    return (g, g, g)