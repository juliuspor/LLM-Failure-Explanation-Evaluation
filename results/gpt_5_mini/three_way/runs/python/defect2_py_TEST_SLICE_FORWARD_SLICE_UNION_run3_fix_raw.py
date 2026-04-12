def get_paint(self, value: float) -> Tuple[int, int, int]:
    # Ensure the scale has non-zero range
    if self._upper_bound == self._lower_bound:
        raise ValueError("Requires lowerBound < upperBound.")

    # Clamp value to bounds
    v = max(self._lower_bound, min(value, self._upper_bound))

    # Compute gray level from clamped value
    g = int((v - self._lower_bound) / (self._upper_bound - self._lower_bound) * 255.0)

    # Clamp g to valid RGB range just in case of rounding
    g = max(0, min(g, 255))

    return (g, g, g)