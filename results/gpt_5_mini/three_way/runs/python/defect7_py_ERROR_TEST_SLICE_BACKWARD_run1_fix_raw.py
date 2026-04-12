@classmethod
def to_class(cls, array: Optional[List[Any]]) -> Optional[List[Type]]:
    if array is None:
        return None
    # Return an empty list for empty input
    if len(array) == 0:
        return ArrayUtils.EMPTY_CLASS_ARRAY.copy()

    classes: List[Type] = []
    for e in array:
        if e is None:
            classes.append(type(None))
        else:
            classes.append(type(e))
    return classes