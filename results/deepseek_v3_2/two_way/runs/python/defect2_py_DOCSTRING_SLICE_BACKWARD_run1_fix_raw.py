    def get_paint(self, value: float) -> Tuple[int, int, int]:
        v = max(value, self._lower_bound)
        v = min(v, self._upper_bound)
        gray = int((v - self._lower_bound) / (self._upper_bound - self._lower_bound) * 255.0)
        if gray < 0 or gray > 255:
            raise ValueError(f"Color parameter outside of expected range: {gray}")
        return (gray, gray, gray)