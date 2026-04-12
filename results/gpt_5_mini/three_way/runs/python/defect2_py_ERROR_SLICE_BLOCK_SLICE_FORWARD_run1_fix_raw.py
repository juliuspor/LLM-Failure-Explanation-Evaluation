def get_paint(self, value: float) -> Tuple[int, int, int]:
    # Clamp value to bounds
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)

    # compute gray level based on clamped v
    g = int((v - self._lower_bound) / (self._upper_bound - self._lower_bound) * 255.0)
    r = g
    b = g

    # validate all components
    if any(component < 0 or component > 255 for component in (r, g, b)):
        raise ValueError("Color parameter outside of expected range: Red Green Blue")

    return (r, g, b)