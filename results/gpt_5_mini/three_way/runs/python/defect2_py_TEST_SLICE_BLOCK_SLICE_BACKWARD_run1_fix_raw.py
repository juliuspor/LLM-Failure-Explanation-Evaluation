def get_paint(self, value: float) -> Tuple[int, int, int]:
    # Clamp value to bounds
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)

    # Normalize to 0.0..1.0 based on the clamped value
    norm = (v - self._lower_bound) / (self._upper_bound - self._lower_bound)

    # Convert to 0..255 and ensure integer within range
    g = int(norm * 255.0)
    g = max(0, min(255, g))

    return (g, g, g)