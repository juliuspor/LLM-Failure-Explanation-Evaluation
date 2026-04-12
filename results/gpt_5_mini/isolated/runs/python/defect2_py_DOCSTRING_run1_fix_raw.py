def get_paint(self, value: float) -> Tuple[int, int, int]:
    # Validate input type
    try:
        # Attempt numeric operations to catch None/NaN early (NaN handled below)
        _ = float(value)
    except Exception:
        raise TypeError("value must be a numeric type")

    # Clamp value to bounds using the bounds stored on the instance
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)

    # Guard against zero range
    range_span = self._upper_bound - self._lower_bound
    if range_span == 0.0:
        raise ValueError("Lower and upper bounds must not be equal")

    # Compute normalized intensity in [0.0, 1.0]
    intensity = (v - self._lower_bound) / float(range_span)
    # Clamp intensity robustly
    intensity = max(0.0, min(1.0, intensity))

    # Convert to 0..255 using rounding to avoid 256 due to floating point
    g = int(round(intensity * 255.0))
    # Final clamp to ensure within 0..255
    g = max(0, min(255, g))

    return (g, g, g)