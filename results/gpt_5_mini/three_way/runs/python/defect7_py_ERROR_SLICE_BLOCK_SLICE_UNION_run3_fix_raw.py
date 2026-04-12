@classmethod
def to_class(cls, array: Optional[List[Any]]) -> Optional[List[Type]]:
    if array is None:
        return None
    elif len(array) == 0:
        return ArrayUtils.EMPTY_CLASS_ARRAY.copy()

    classes: List[Type] = []
    for i in range(len(array)):
        value = array[i]
        if value is None:
            classes.append(type(None))
            continue
        # Preserve the original behavior of attempting to call upper() on string-like values
        # but guard against non-string objects that don't provide upper().
        if hasattr(value, 'upper') and callable(getattr(value, 'upper')):
            try:
                _ = value.upper()
            except Exception:
                # ignore any exception from upper(), it's not essential for determining the type
                pass
        classes.append(type(value))
    return classes