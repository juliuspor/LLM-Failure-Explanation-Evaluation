    @classmethod
    def to_class(cls, array: Optional[List[Any]]) -> Optional[List[Type]]:
        """
        Converts an array of Object to an array of Class objects.
        If any of these objects is None, a None element will be inserted into the array.

        This method returns None for a None input array.

        Args:
            array: an Object array

        Returns:
            a Class array, None if None array input

        Raises:
            AttributeError: If any element is None
        """
        if array is None:
            return None
        elif len(array) == 0:
            return ArrayUtils.EMPTY_CLASS_ARRAY.copy()

        classes = []
        for i in range(len(array)):
            if array[i] is None:
                classes.append(None)
            else:
                classes.append(type(array[i]))
        return classes
