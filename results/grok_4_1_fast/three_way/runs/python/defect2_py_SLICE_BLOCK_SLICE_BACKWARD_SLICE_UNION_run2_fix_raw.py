    def get_paint(self, value: float) -> Tuple[int, int, int]:
        # Clamp value to bounds
        v = max(value, self._lower_bound)
        v = min(v, self._upper_bound)
        
        # Normalize and clamp to prevent floating-point precision issues
        normalized = (v - self._lower_bound) / (self._upper_bound - self._lower_bound)
        normalized = max(0.0, min(1.0, normalized))
        g = int(normalized * 255.0)
        
        return (g, g, g)