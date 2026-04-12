@classmethod
def to_class(cls, array: Optional[List[Any]]) -> Optional[List[Type]]:
    if array is None:
        return None
    elif len(array) == 0:
        return ArrayUtils.EMPTY_CLASS_ARRAY.copy()
    classes = []
    for item in array:
        if item is None:
            classes.append(type(None))
            continue
        try:
            classes.append(type(item))
        except Exception:
            classes.append(None)
    return classes
