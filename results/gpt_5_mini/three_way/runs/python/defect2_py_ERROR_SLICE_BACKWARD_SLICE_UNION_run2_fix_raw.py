def get_paint(self, value: float) -> Tuple[int, int, int]:
    # Clamp value to bounds
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)

    # Compute normalized gray using the clamped value to ensure result in 0..255
    range_width = self._upper_bound - self._lower_bound
    if range_width == 0.0:
        # Should not happen because constructor prevents lower>=upper, but guard defensively
        raise ValueError("Invalid paint scale with zero range.")

    g = int((v - self._lower_bound) / range_width * 255.0)

    # Ensure within bounds (defensive)
    if g < 0 or g > 255:
        raise ValueError(f"Color parameter outside of expected range: computed gray={g}, value={value}, bounds=({self._lower_bound},{self._upper_bound})")

    return (g, g, g)