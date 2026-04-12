@classmethod
    def to_class(cls, array: Optional[List[Any]]) -> Optional[List[Type]]:
        if array is None:
            return None
        elif len(array) == 0:
            return ArrayUtils.EMPTY_CLASS_ARRAY.copy()
        classes = []
        for i in range(len(array)):
            elem = array[i]
            # Do not call methods on elements (like .upper()) which assume a specific type.
            # If element is None, preserve as type(None).
            classes.append(type(elem))
        return classes
