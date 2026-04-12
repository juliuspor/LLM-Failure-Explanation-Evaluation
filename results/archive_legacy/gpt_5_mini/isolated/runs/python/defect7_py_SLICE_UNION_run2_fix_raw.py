@classmethod
def to_class(cls, array: Optional[List[Any]]) -> Optional[List[Type]]:
    if array is None:
        return None
    elif len(array) == 0:
        return ArrayUtils.EMPTY_CLASS_ARRAY.copy()

    classes = []
    for i in range(len(array)):
        val = array[i]
        if isinstance(val, str):
            _ = val.upper()
        else:
            _ = None
        classes.append(type(val))
    return classes
