def get_paint(self, value: float) -> Tuple[int, int, int]:
    # Clamp value to bounds
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)

    # Compute gray level using the clamped value
    g = int((v - self._lower_bound) / (self._upper_bound - self._lower_bound) * 255.0)

    # Validate the computed component is in the expected range
    if g < 0 or g > 255:
        raise ValueError(f"Color parameter outside of expected range: g={g}, value={value}, clamped_value={v}")

    return (g, g, g)