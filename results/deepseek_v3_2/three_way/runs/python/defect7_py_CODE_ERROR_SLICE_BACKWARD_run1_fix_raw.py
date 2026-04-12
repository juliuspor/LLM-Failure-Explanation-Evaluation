    @classmethod
    def to_class(cls, array: Optional[List[Any]]) -> Optional[List[Type]]:
        """
        Convert a list of objects to a list of their classes.

        Args:
            array: the list of objects, may be None.

        Returns:
            A list of Python `type` objects corresponding to the input elements,
            or None if `array` is None.
        """
        if array is None:
            return None
        if len(array) == 0:
            return ArrayUtils.EMPTY_CLASS_ARRAY.copy()
        
        classes = []
        for obj in array:
            classes.append(type(obj))
        return classes