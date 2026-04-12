def get_paint(self, value: float) -> Tuple[int, int, int]:
    # Clamp value to bounds
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)

    # Map clamped value into 0..255 range, using rounding to nearest integer
    mapped = (v - self._lower_bound) / (self._upper_bound - self._lower_bound) * 255.0
    component = int(round(mapped))

    # Clamp component to valid 0..255 range
    component = max(0, min(255, component))

    # Final validation (should always pass after clamping)
    if component < 0 or component > 255:
        raise ValueError(f"Color parameter outside of expected range: {component}")

    return (component, component, component)