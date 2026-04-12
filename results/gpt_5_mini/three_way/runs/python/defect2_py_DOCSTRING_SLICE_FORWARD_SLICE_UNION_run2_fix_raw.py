def get_paint(self, value: float) -> Tuple[int, int, int]:
    # Validate span to avoid division by zero
    span = self._upper_bound - self._lower_bound
    if span == 0.0:
        raise ValueError("GrayPaintScale has zero span (lower_bound == upper_bound).")

    # Clamp value to bounds
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)

    # Normalize to [0.0, 1.0] using the clamped value, then scale to 0..255
    norm = (v - self._lower_bound) / span
    # Ensure numerical robustness by clamping the normalized value
    norm = max(0.0, min(1.0, norm))

    g = int(norm * 255.0)

    # In Python, we validate the range (Java Color constructor does this)
    if g < 0 or g > 255:
        raise ValueError(f"Color parameter outside of expected range: g={g}")

    return (g, g, g)