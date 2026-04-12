def get_paint(self, value: float) -> Tuple[int, int, int]:
    # Clamp value to bounds
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)

    # Guard against division by zero though constructor prevents equal bounds
    range_ = (self._upper_bound - self._lower_bound)
    if range_ == 0.0:
        raise ValueError("Invalid GrayPaintScale with zero range (lower_bound == upper_bound)")

    # Compute gray level using the clamped value and ensure it's within 0..255
    computed = (v - self._lower_bound) / range_ * 255.0
    g = int(round(computed))
    g = max(0, min(255, g))

    return (g, g, g)