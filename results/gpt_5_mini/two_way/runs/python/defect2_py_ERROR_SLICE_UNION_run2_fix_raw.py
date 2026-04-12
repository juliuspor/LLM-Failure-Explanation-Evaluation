def get_paint(self, value: float) -> Tuple[int, int, int]:
    # Clamp value to bounds
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)

    # Compute normalized ratio safely and clamp to [0.0, 1.0]
    span = (self._upper_bound - self._lower_bound)
    if span == 0.0:
        ratio = 0.0
    else:
        ratio = (v - self._lower_bound) / span
    ratio = max(0.0, min(1.0, ratio))

    g = int(ratio * 255.0)

    # Validate range for safety
    if g < 0 or g > 255:
        raise ValueError(f"Computed gray level {g} out of range 0..255 for input value={value} (clamped to {v}) and bounds=({self._lower_bound},{self._upper_bound})")

    return (g, g, g)