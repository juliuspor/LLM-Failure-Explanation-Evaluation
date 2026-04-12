@classmethod
    def to_class(cls, array: Optional[List[Any]]) -> Optional[List[Type]]:
        if array is None:
            return None
        elif len(array) == 0:
            return ArrayUtils.EMPTY_CLASS_ARRAY.copy()
        
        classes: List[Type] = []
        for elem in array:
            if elem is None:
                classes.append(type(None))
            else:
                classes.append(type(elem))
        return classes
