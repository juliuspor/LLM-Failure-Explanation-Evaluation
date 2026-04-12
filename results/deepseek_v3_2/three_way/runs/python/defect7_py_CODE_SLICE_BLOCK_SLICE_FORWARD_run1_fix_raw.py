    @classmethod
    def to_class(cls, array: Optional[List[Any]]) -> Optional[List[Type]]:
        """
        Convert a list of objects to a list of their corresponding classes.

        Args:
            array: Sequence of objects. May be None.
            
        Returns:
            A list of Python types, or None if input is None.
        """
        if array is None:
            return None
        elif len(array) == 0:
            return ArrayUtils.EMPTY_CLASS_ARRAY
        
        classes = []
        for i in range(len(array)):
            classes.append(type(array[i]))
        return classes