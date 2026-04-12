@classmethod
def to_class(cls, array: Optional[List[Any]]) -> Optional[List[Type]]:
    if array is None:
        return None
    elif len(array) == 0:
        return ArrayUtils.EMPTY_CLASS_ARRAY.copy()

    classes = []
    for item in array:
        if item is None:
            classes.append(None)
            continue
        # Only call upper if item is a string; otherwise skip the upper call
        if isinstance(item, str):
            _ = item.upper()
        classes.append(type(item))
    return classes
