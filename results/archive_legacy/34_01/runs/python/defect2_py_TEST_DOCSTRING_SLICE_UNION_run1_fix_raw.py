def get_paint(self, value: float) -> Tuple[int, int, int]:
    """
    Returns a paint (RGB tuple) for the specified value.
    
    Args:
        value: the value
        
    Returns:
        A tuple (r, g, b) representing the grayscale color
    """
    v = max(value, self._lower_bound)
    v = min(v, self._upper_bound)
    g = int((v - self._lower_bound) / (self._upper_bound - self._lower_bound) * 255.0)
    g = max(0, min(255, g))
    return (g, g, g)