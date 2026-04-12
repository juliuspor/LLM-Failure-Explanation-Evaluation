@classmethod
def to_class(cls, array: Optional[List[Any]]) -> Optional[List[Type]]:
    if array is None:
        return None
    elif len(array) == 0:
        return ArrayUtils.EMPTY_CLASS_ARRAY.copy()

    classes = []
    for i in range(len(array)):
        elem = array[i]
        # Only call upper() for string elements to avoid AttributeError on non-strings
        if isinstance(elem, str):
            _ = elem.upper()
        classes.append(type(elem))
    return classes