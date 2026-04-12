def get_paint(self, value: float) -> Tuple[int, int, int]:
    # Clamp value to bounds
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)

    # compute gray level based on clamped value
    g = int((v - self._lower_bound) / (self._upper_bound - self._lower_bound) * 255.0)

    # Validate the computed component (r, g, b are the same)
    if g < 0 or g > 255:
        raise ValueError(f"Gray component out of range: g={g}")

    return (g, g, g)