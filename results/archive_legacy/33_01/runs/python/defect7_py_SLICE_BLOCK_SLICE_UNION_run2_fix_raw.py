@classmethod
def to_class(cls, array: Optional[List[Any]]) -> Optional[List[Type]]:
    if array is None:
        return None
    if len(array) == 0:
        return ArrayUtils.EMPTY_CLASS_ARRAY.copy()
    classes = []
    for i in range(len(array)):
        if array[i] is None:
            raise AttributeError("Array element at index %d is None" % i)
        classes.append(type(array[i]))
    return classes
