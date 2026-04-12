def get_paint(self, value: float) -> Tuple[int, int, int]:
    # Clamp value to bounds
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)

    # Defensive check to avoid division by zero (should be prevented by __init__)
    range_span = self._upper_bound - self._lower_bound
    if range_span == 0.0:
        raise ValueError("GrayPaintScale has zero range (upper_bound == lower_bound)")

    # Compute gray level based on clamped value
    g = int((v - self._lower_bound) / range_span * 255.0)

    # Ensure components are within 0..255
    r = g
    b = g

    if not (0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255):
        raise ValueError(f"Color component out of range for input value={value}: (r={r}, g={g}, b={b})")

    return (r, g, b)