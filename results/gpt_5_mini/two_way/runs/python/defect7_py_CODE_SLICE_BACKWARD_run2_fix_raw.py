@classmethod
def to_class(cls, array: Optional[List[Any]]) -> Optional[List[Type]]:
    if array is None:
        return None
    elif len(array) == 0:
        return ArrayUtils.EMPTY_CLASS_ARRAY.copy()

    classes: List[Optional[Type]] = []
    for val in array:
        if val is None:
            # Preserve None entries as None to mirror Java behavior where null maps to null
            classes.append(None)
        else:
            # Determine the type of the value
            classes.append(type(val))
    return classes