def get_paint(self, value: float) -> tuple:
    # Clamp value to bounds
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)

    denom = (self._upper_bound - self._lower_bound)
    if denom == 0.0:
        raise ValueError(f"Invalid GrayPaintScale with zero range: lower_bound={self._lower_bound}, upper_bound={self._upper_bound}")

    # Use the clamped value 'v' for normalization
    g = int((v - self._lower_bound) / denom * 255.0)

    # Validate the computed component
    if g < 0 or g > 255:
        raise ValueError(f"Computed grayscale component out of range: g={g} (expected 0..255) for input value={value} clamped to {v}")

    return (g, g, g)