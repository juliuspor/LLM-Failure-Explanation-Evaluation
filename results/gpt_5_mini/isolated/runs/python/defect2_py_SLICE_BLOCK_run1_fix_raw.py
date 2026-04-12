def get_paint(self, value: float) -> Tuple[int, int, int]:
    # Clamp value to bounds
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)

    # Compute gray level using the clamped value
    g = int((v - self._lower_bound) / (self._upper_bound - self._lower_bound) * 255.0)

    # Validate the computed channel
    def _check_channel(name: str, val: int) -> None:
        if not (0 <= val <= 255):
            raise ValueError(f"Color parameter '{name}' out of range: {val} (expected 0-255)")

    _check_channel('gray', g)
    return (g, g, g)