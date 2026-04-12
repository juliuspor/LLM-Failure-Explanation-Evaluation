    def get_paint(self, value: float) -> Tuple[int, int, int]:
        v = max(value, self._lower_bound)
        v = min(v, self._upper_bound)
        
        g = (v - self._lower_bound) / (self._upper_bound - self._lower_bound) * 255.0
        g = max(0.0, min(g, 255.0))
        g_int = int(round(g))
        
        if g_int < 0 or g_int > 255:
            raise ValueError(f"Color parameter outside of expected range: {g_int} {g_int} {g_int}")
        
        return (g_int, g_int, g_int)