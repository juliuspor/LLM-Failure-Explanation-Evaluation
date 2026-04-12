    @classmethod
    def to_class(cls, array: Optional[List[Any]]) -> Optional[List[Type]]:
        """
        Convert a list of objects to a list of their types.

        Args:
            array: the list of objects, may be None

        Returns:
            a list of types, or None if input is None
        """
        if array is None:
            return None
        classes = []
        for i in range(len(array)):
            classes.append(type(array[i]))
        return classes