def get_paint(self, value: float) -> Tuple[int, int, int]:
    # Clamp value to bounds
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)

    denom = (self._upper_bound - self._lower_bound)
    if denom == 0.0:
        # Should not happen because constructor prevents equal bounds, but guard anyway
        raise ValueError("Invalid scale with zero range.")

    # Map the clamped value to a gray level 0..255
    gray = int((v - self._lower_bound) / denom * 255.0)

    # Validate the computed component
    if gray < 0 or gray > 255:
        raise ValueError(f"Color parameter outside of expected range: gray={gray}")

    return (gray, gray, gray)