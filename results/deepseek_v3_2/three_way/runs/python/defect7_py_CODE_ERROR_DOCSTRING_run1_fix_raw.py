    @classmethod
    def to_class(cls, array: Optional[List[Any]]) -> Optional[List[Type]]:
        """
        Convert a list of objects to a list of their classes.

        Args:
            array: the list of objects, may be None

        Returns:
            a list of classes corresponding to the objects,
            None if None input, empty list if empty input
        """
        if array is None:
            return None
        elif len(array) == 0:
            return ArrayUtils.EMPTY_CLASS_ARRAY.copy()
        
        classes = []
        for element in array:
            classes.append(type(element))
        return classes