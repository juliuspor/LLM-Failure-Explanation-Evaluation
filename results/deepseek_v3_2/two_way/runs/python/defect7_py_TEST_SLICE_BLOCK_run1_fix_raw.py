    @classmethod
    def to_class(cls, array: Optional[List[Any]]) -> Optional[List[Type]]:
        """
        Convert a list of objects to a list of their classes.

        Args:
            array: List of objects. If None, returns None.

        Returns:
            List of types corresponding to each object.
        """
        if array is None:
            return None
        if len(array) == 0:
            return ArrayUtils.EMPTY_CLASS_ARRAY.copy()
        classes = []
        for i in range(len(array)):
            classes.append(type(array[i]))
        return classes