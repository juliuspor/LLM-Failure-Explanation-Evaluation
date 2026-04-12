def get_paint(self, value: float) -> Tuple[int, int, int]:
    # Clamp value to bounds
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)

    # Handle zero range defensively: return mid-gray (or lower bound color)
    range_span = self._upper_bound - self._lower_bound
    if range_span == 0.0:
        # If bounds are equal, treat as midpoint gray
        g = 128
    else:
        # Normalize using the clamped value 'v'
        fraction = (v - self._lower_bound) / range_span
        # Compute gray component, round to nearest int and clamp to 0..255
        g = int(round(fraction * 255.0))
        if g < 0:
            g = 0
        elif g > 255:
            g = 255

    return (g, g, g)