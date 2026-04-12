def get_paint(self, value: float) -> Tuple[int, int, int]:
    # Clamp value to bounds
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)

    # Calculate the gray component using the clamped value
    component = int((v - self._lower_bound) / (self._upper_bound - self._lower_bound) * 255.0)

    # Validate the component is within 0..255
    if component < 0 or component > 255:
        raise ValueError(f"Color component outside of expected range: {component}")

    r = g = b = component
    return (r, g, b)