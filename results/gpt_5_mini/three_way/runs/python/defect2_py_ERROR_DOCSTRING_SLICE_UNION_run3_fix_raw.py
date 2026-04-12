def get_paint(self, value: float) -> Tuple[int, int, int]:
    # Clamp value to bounds (respecting the docstring)
    v = max(self._lower_bound, min(value, self._upper_bound))

    # Guard against division by zero (should not happen due to constructor, but be defensive)
    span = self._upper_bound - self._lower_bound
    if span == 0.0:
        # Return middle gray if bounds are degenerate
        g = 127
        return (g, g, g)

    # Compute gray level from the clamped value
    g = int((v - self._lower_bound) / span * 255.0)

    # Ensure g is within the valid byte range
    if g < 0 or g > 255:
        raise ValueError(f"Computed gray value out of range: {g}")

    return (g, g, g)