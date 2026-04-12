@classmethod
    def to_class(cls, array: Optional[List[Any]]) -> Optional[List[Type]]:
        if array is None:
            return None
        elif len(array) == 0:
            return ArrayUtils.EMPTY_CLASS_ARRAY.copy()
        classes = []
        for val in array:
            # Do not assume elements are strings; simply record their types.
            classes.append(type(val))
        return classes