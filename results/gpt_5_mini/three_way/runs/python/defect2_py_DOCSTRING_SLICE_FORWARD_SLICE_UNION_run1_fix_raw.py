def get_paint(self, value: float) -> Tuple[int, int, int]:
    # Clamp value to bounds
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)

    denom = (self._upper_bound - self._lower_bound)
    if denom == 0.0:
        # Fall back to middle gray if bounds are degenerate
        ratio = 0.5
    else:
        ratio = (v - self._lower_bound) / denom

    g = int(ratio * 255.0)

    # Ensure g is within 0..255
    if g < 0 or g > 255:
        raise ValueError(f"Computed color component out of range: {g} (expected 0..255). value={value}, clamped={v}, bounds=({self._lower_bound},{self._upper_bound})")

    return (g, g, g)