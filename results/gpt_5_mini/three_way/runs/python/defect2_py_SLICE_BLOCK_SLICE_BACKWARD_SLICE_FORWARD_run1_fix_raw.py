def get_paint(self, value: float) -> Tuple[int, int, int]:
    # Clamp value to bounds
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)

    # Safe denominator (constructor guarantees lower < upper)
    denom = (self._upper_bound - self._lower_bound)
    # Compute gray level based on clamped value
    g = int((v - self._lower_bound) / denom * 255.0)

    # Ensure g is within valid RGB component range
    if g < 0 or g > 255:
        raise ValueError(f"Computed color component out of range: g={g} (expected 0..255); value={value}, clamped_value={v}, bounds=({self._lower_bound},{self._upper_bound})")

    return (g, g, g)