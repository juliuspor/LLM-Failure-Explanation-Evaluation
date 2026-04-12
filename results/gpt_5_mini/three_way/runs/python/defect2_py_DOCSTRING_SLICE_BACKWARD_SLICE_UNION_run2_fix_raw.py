def get_paint(self, value: float) -> Tuple[int, int, int]:
    # Clamp value to bounds
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)

    # Ensure denominator is not zero (should be guaranteed by constructor, but check defensively)
    denom = self._upper_bound - self._lower_bound
    if denom == 0.0:
        raise ValueError("Scale bounds must differ (upper_bound != lower_bound)")

    # Normalize and scale to 0..255
    gray = int((v - self._lower_bound) / denom * 255.0)

    # Clamp gray to valid byte range
    if gray < 0 or gray > 255:
        raise ValueError(f"Color component outside 0..255: {gray}")

    return (gray, gray, gray)