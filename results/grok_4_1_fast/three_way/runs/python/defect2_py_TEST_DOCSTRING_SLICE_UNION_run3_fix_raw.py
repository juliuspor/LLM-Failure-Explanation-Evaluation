    def get_paint(self, value: float) -> Tuple[int, int, int]:
        # Clamp value to bounds
        v = max(value, self._lower_bound)
        v = min(v, self._upper_bound)
        
        g = int((v - self._lower_bound) / (self._upper_bound - self._lower_bound) * 255.0)
        
        # Clamp to valid range
        g = max(0, min(255, g))
        
        return (g, g, g)