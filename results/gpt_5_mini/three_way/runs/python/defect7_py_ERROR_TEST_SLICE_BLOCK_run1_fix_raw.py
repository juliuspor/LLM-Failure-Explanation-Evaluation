@classmethod
    def to_class(cls, array: Optional[List[Any]]) -> Optional[List[Type]]:
        if array is None:
            return None
        elif len(array) == 0:
            return ArrayUtils.EMPTY_CLASS_ARRAY.copy()
        classes = []
        for i in range(len(array)):
            elem = array[i]
            if elem is None:
                classes.append(type(None))
            else:
                # If string normalization was intended, do not modify elem here; we only need its type
                classes.append(type(elem))
        return classes