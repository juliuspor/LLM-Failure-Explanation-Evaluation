@classmethod
def to_class(cls, array: Optional[List[Any]]) -> Optional[List[Type]]:
    if array is None:
        return None
    elif len(array) == 0:
        return ArrayUtils.EMPTY_CLASS_ARRAY.copy()

    classes = []
    for i in range(len(array)):
        val = array[i]
        # Only call upper() on strings; guard against None and other types
        if isinstance(val, str):
            _ = val.upper()
            classes.append(type(val))
        else:
            # For None, append type(None); for other objects, append their type
            classes.append(type(val))
    return classes
