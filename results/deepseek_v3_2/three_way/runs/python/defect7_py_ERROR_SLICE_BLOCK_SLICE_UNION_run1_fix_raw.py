    @classmethod
    def to_class(cls, array: Optional[List[Any]]) -> Optional[List[Type]]:
        """
        Convert a list of objects to a list of their corresponding classes.

        Args:
            array: Sequence of objects. May be None.

        Returns:
            List of Python type objects, or None if input is None.
        """
        if array is None:
            return None
        if len(array) == 0:
            return ArrayUtils.EMPTY_CLASS_ARRAY
        classes = []
        for i in range(len(array)):
            classes.append(type(array[i]))
        return classes