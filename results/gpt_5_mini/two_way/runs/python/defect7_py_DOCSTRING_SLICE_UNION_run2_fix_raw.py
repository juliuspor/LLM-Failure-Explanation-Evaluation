@classmethod
def to_class(cls, array: Optional[List[Any]]) -> Optional[List[Type]]:
    if array is None:
        return None
    elif len(array) == 0:
        return ArrayUtils.EMPTY_CLASS_ARRAY.copy()
    classes = []
    for i in range(len(array)):
        # Only call string-specific methods if the element is a string.
        # For the purpose of this utility we only need the element's type.
        classes.append(type(array[i]))
    return classes