    def get_paint(self, value: float) -> Tuple[int, int, int]:
        # Clamp value to bounds
        v = max(value, self._lower_bound)
        v = min(v, self._upper_bound)
        
        if self._lower_bound == self._upper_bound:
            g = 0
        else:
            g = int((v - self._lower_bound) / (self._upper_bound - self._lower_bound) * 255.0)
        
        return (g, g, g)