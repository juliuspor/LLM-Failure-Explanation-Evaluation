@classmethod
    def to_class(cls, array: Optional[List[Any]]) -> Optional[List[Type]]:
        if array is None:
            return None
        elif len(array) == 0:
            return ArrayUtils.EMPTY_CLASS_ARRAY.copy()
        
        classes = []
        for i in range(len(array)):
            element = array[i]
            if element is None:
                classes.append(type(None))
            else:
                classes.append(type(element))
        return classes