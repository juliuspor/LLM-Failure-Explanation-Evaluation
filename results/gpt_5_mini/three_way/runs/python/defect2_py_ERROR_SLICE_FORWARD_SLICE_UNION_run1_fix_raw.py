def get_paint(self, value: float) -> Tuple[int, int, int]:
    # Clamp value to bounds
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)

    # If original value was out of bounds, raise a clear error
    if not (self._lower_bound <= value <= self._upper_bound):
        raise ValueError(f"value {value} out of range [{self._lower_bound}, {self._upper_bound}]")

    # Compute gray level using the clamped value
    g = int((v - self._lower_bound) / (self._upper_bound - self._lower_bound) * 255.0)

    # Ensure g is within 0..255
    g = max(0, min(255, g))

    return (g, g, g)