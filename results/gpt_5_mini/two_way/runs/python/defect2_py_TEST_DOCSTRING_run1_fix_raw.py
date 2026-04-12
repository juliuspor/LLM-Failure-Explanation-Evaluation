def get_paint(self, value: float) -> Tuple[int, int, int]:
    import math

    # Handle non-finite inputs by treating them as lower bound
    if not math.isfinite(value):
        v = self._lower_bound
    else:
        v = value

    # Clamp value to bounds
    if v < self._lower_bound:
        v = self._lower_bound
    if v > self._upper_bound:
        v = self._upper_bound

    # Handle degenerate case to avoid division by zero
    if self._upper_bound == self._lower_bound:
        fraction = 0.0
    else:
        fraction = (v - self._lower_bound) / (self._upper_bound - self._lower_bound)

    # Ensure numerical safety: clamp fraction to [0.0, 1.0]
    if fraction < 0.0:
        fraction = 0.0
    elif fraction > 1.0:
        fraction = 1.0

    # Compute gray value, use round then clamp to 0..255
    gray = int(round(fraction * 255.0))
    if gray < 0:
        gray = 0
    elif gray > 255:
        gray = 255

    return (gray, gray, gray)