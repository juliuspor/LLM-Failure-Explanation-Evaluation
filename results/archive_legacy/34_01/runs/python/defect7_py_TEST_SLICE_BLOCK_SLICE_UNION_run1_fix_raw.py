@classmethod
def to_class(cls, array: Optional[List[Any]]) -> Optional[List[Type]]:
    if array is None:
        return None
    elif len(array) == 0:
        return ArrayUtils.EMPTY_CLASS_ARRAY.copy()
    classes = []
    for val in array:
        if val is None:
            classes.append(type(None))
            continue
        if isinstance(val, str):
            _ = val.upper()
        classes.append(type(val))
    return classes