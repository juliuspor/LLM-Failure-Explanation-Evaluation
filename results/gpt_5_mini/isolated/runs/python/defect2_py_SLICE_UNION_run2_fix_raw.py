def get_paint(self, value: float) -> Tuple[int, int, int]:
    # Clamp value to bounds
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)

    range_span = self._upper_bound - self._lower_bound
    if range_span == 0.0:
        raise ValueError("Invalid paint scale with zero range between bounds.")

    # compute gray level from the clamped value
    grey = int((v - self._lower_bound) / range_span * 255.0)

    # validate
    if grey < 0 or grey > 255:
        raise ValueError(f"Color component out of range: grey={grey}")

    return (grey, grey, grey)