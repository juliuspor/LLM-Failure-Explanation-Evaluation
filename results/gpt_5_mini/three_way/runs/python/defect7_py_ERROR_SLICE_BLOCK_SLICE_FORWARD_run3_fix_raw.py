@classmethod
def to_class(cls, array: Optional[List[Any]]) -> Optional[List[Type]]:
    if array is None:
        return None
    elif len(array) == 0:
        return ArrayUtils.EMPTY_CLASS_ARRAY.copy()

    classes = []
    for v in array:
        if v is None:
            classes.append(type(None))
        else:
            # Avoid calling methods on objects that may not have them.
            # Preserve legacy behavior of upper-casing strings if needed but do not rely on it.
            if isinstance(v, str):
                _ = v.upper()
            classes.append(type(v))
    return classes