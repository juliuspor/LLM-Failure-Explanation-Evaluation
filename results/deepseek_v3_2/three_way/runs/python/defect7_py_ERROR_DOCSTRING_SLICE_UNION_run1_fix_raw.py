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
            # The original bug: calling .upper() on array[i] without checking for None
            # We should simply get the type of each element, handling None as a valid element.
            # The .upper() call seems to be a leftover from some other logic and is unnecessary.
            # Remove the .upper() call and directly get the type.
            element = array[i]
            classes.append(type(element))
        return classes