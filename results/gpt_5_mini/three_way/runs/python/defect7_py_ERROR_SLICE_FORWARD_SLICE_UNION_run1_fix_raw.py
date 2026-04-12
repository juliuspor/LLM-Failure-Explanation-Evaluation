@classmethod
    def to_class(cls, array: Optional[List[Any]]) -> Optional[List[Type]]:
        if array is None:
            return None
        elif len(array) == 0:
            return ArrayUtils.EMPTY_CLASS_ARRAY.copy()
        
        classes = []
        for i in range(len(array)):
            elem = array[i]
            # Avoid calling string methods on None or non-string types
            if elem is None:
                classes.append(type(None))
            else:
                # original code called .upper() but did not use the result; drop it
                classes.append(type(elem))
        return classes