def get_paint(self, value: float) -> Tuple[int, int, int]:
    # Clamp value to bounds
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)

    # Normalize using the clamped value
    denom = (self._upper_bound - self._lower_bound)
    # denom should never be zero because __init__ validates bounds, but guard defensively
    if denom == 0.0:
        raise ValueError(f"Invalid bounds: lower_bound ({self._lower_bound}) and upper_bound ({self._upper_bound}) must differ.")

    g = int((v - self._lower_bound) / denom * 255.0)

    # Ensure g is in the valid byte range (defensive clamp)
    if g < 0:
        g = 0
    elif g > 255:
        g = 255

    # Additional sanity check (should not trigger)
    if g < 0 or g > 255:
        raise ValueError(f"Computed gray value out of range: g={g}, value={value}, lower={self._lower_bound}, upper={self._upper_bound}")

    return (g, g, g)