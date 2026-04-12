def get_paint(self, value: float) -> Tuple[int, int, int]:
    # Clamp value to bounds
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)

    # Compute gray level based on the clamped value
    denom = (self._upper_bound - self._lower_bound)
    if denom == 0.0:
        # Shouldn't happen because constructor prevents it, but guard anyway
        raise ValueError("Invalid GrayPaintScale with zero range.")

    g = int((v - self._lower_bound) / denom * 255.0)

    # Validate the range (similar to Java Color constructor behavior)
    if g < 0 or g > 255:
        raise ValueError(f"Color parameter outside of expected range: g={g}, value={v}, bounds=({self._lower_bound},{self._upper_bound})")

    return (g, g, g)