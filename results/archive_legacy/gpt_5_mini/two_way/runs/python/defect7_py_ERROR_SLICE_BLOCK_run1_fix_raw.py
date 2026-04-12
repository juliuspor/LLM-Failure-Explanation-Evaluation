@classmethod
def to_class(cls, array: Optional[List[Any]]) -> Optional[List[Type]]:
    if array is None:
        return None
    elif len(array) == 0:
        return ArrayUtils.EMPTY_CLASS_ARRAY.copy()
    classes = []
    for i in range(len(array)):
        if array[i] is None:
            raise AttributeError(f"Parameter array[{i}] must not be None")
        classes.append(type(array[i]))
    return classes