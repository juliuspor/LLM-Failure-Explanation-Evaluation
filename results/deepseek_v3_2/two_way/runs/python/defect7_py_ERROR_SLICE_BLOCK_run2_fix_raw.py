    @classmethod
    def to_class(cls, array: Optional[List[Any]]) -> Optional[List[Type]]:
        """
        Convert a list of objects to a list of their corresponding classes.

        Args:
            array: Sequence of objects. If None, returns None.
            
        Returns:
            A list of Python `type` objects corresponding to the input elements, or
            None if `array` is None.
        """
        if array is None:
            return None
        elif len(array) == 0:
            return ArrayUtils.EMPTY_CLASS_ARRAY.copy()
        
        classes = []
        for i in range(len(array)):
            # The original bug: array[i].upper() assumes array[i] is a string.
            # But array[i] could be None or any other type.
            # We should simply get the type of the element.
            # So we remove the .upper() call and directly get type.
            classes.append(type(array[i]))
        return classes