        # Clamp value to bounds
        v = max(value, self._lower_bound)
        v = min(v, self._upper_bound)
        
        g = int((v - self._lower_bound) / (self._upper_bound - self._lower_bound) * 255.0)
        
        # In Python, we validate the range (Java Color constructor does this)
        if g < 0 or g > 255:
            raise ValueError(f"Grayscale value outside of expected range: {g}")
        
        return (g, g, g)