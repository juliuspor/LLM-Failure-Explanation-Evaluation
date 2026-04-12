def get_paint(self, value: float) -> Tuple[int, int, int]:
    # Clamp value to bounds
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)

    # Normalize to 0..1 using the clamped value to avoid out-of-range results
    denom = (self._upper_bound - self._lower_bound)
    # denom should never be zero because __init__ enforces lower < upper
    t = (v - self._lower_bound) / denom

    # Map to 0..255
    g = int(t * 255.0)

    # Ensure g is within valid byte range (defensive)
    if g < 0 or g > 255:
        raise ValueError(f"Color parameter out of range for green: g={g}, expected 0..255, computed from value={value}, bounds=({self._lower_bound},{self._upper_bound})")

    return (g, g, g)