def get_paint(self, value: float) -> Tuple[int, int, int]:
    # Clamp value to bounds
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)

    # Prevent division by zero (shouldn't happen because constructor enforces bounds,
    # but guard defensively in case of tampering)
    range_span = self._upper_bound - self._lower_bound
    if range_span == 0.0:
        raise ValueError("Invalid GrayPaintScale: upper_bound equals lower_bound, division by zero")

    # Compute gray component from the clamped value
    comp = int((v - self._lower_bound) / range_span * 255.0)

    # Validate the computed component
    if comp < 0 or comp > 255:
        raise ValueError(f"Color parameter outside of expected range: component={comp}")

    return (comp, comp, comp)