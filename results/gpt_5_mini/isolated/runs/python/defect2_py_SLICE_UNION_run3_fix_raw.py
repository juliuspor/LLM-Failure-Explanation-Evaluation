def get_paint(self, value: float) -> Tuple[int, int, int]:
    # Validate that value is a number and within bounds
    if value < self._lower_bound or value > self._upper_bound:
        raise ValueError(f"Value {value} outside of bounds [{self._lower_bound}, {self._upper_bound}]")

    # Normalize value to 0..1 within bounds
    range_span = self._upper_bound - self._lower_bound
    if range_span == 0.0:
        # Should not happen because constructor prevents equal bounds, but guard anyway
        normalized = 0.0
    else:
        normalized = (value - self._lower_bound) / range_span

    # Compute gray component 0..255
    g = int(normalized * 255.0)

    # Ensure components are within 0..255
    r = g
    b = g
    out_of_range = []
    if r < 0 or r > 255:
        out_of_range.append(f"r={r}")
    if g < 0 or g > 255:
        out_of_range.append(f"g={g}")
    if b < 0 or b > 255:
        out_of_range.append(f"b={b}")
    if out_of_range:
        raise ValueError(
            f"Color component(s) out of range for value={value} bounds=[{self._lower_bound}, {self._upper_bound}]: "
            + ", ".join(out_of_range)
        )

    return (r, g, b)