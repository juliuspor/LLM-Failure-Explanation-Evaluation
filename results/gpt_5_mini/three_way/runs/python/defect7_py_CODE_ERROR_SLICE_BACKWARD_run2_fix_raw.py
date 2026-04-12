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
                classes.append(None)
            else:
                # If it's a string that represents a class name, attempt to resolve it
                if isinstance(elem, str):
                    try:
                        # Try to resolve string class name to actual class
                        classes.append(cls.get_class(elem))
                    except Exception:
                        # Fallback to using type of the string
                        classes.append(type(elem))
                else:
                    classes.append(type(elem))
        return classes