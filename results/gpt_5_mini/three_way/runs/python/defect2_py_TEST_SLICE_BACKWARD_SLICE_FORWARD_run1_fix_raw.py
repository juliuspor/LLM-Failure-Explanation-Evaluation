def get_paint(self, value: float) -> Tuple[int, int, int]:
    # Clamp value to bounds
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)

    # Use the clamped value to compute the gray level
    g = int((v - self._lower_bound) / (self._upper_bound - self._lower_bound) * 255.0)

    # Ensure g is within valid RGB range (0..255)
    if g < 0 or g > 255:
        raise ValueError(
            f"Computed gray level out of range: {g} (expected 0..255) for value={value}, clamped_value={v}, bounds=({self._lower_bound},{self._upper_bound})"
        )

    return (g, g, g)