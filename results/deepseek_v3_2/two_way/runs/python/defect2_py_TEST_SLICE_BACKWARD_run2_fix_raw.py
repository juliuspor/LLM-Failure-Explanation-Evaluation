    def get_paint(self, value: float) -> Tuple[int, int, int]:
        v = max(value, self._lower_bound)
        v = min(v, self._upper_bound)
        g = int((v - self._lower_bound) / (self._upper_bound - self._lower_bound) * 255.0)
        g = max(0, min(g, 255))
        return (g, g, g)