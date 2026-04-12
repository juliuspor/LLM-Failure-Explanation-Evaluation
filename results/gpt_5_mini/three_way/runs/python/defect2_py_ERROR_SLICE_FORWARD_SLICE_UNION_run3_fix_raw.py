def get_paint(self, value: float) -> Tuple[int, int, int]:
    # Clamp value to bounds to ensure mapping stays within 0..255
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)

    # Compute ratio in [0.0, 1.0]; __init__ guarantees denominator != 0
    ratio = (v - self._lower_bound) / (self._upper_bound - self._lower_bound)
    # Guard against any floating point rounding error
    ratio = max(0.0, min(1.0, ratio))

    # Map to 0..255 and round to nearest integer
    g = int(round(ratio * 255.0))

    # Validate range and provide a clear error if something unexpected occurs
    if g < 0 or g > 255:
        raise ValueError(f"Computed gray component out of range: g={g} for input value={value}, clamped value={v}, bounds=({self._lower_bound},{self._upper_bound})")

    return (g, g, g)