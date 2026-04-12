@classmethod
def to_class(cls, array: Optional[List[Any]]) -> Optional[List[Type]]:
    if array is None:
        return None
    if len(array) == 0:
        return ArrayUtils.EMPTY_CLASS_ARRAY.copy()
    classes = []
    for elem in array:
        if elem is None:
            raise AttributeError("Element " + str(elem) + " is None")
        classes.append(type(elem))
    return classes
