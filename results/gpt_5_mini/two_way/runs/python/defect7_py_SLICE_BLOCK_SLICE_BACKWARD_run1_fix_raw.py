@classmethod
def to_class(cls, array: Optional[List[Any]]) -> Optional[List[Type]]:
    if array is None:
        return None
    elif len(array) == 0:
        return ArrayUtils.EMPTY_CLASS_ARRAY.copy()

    classes = []
    for i in range(len(array)):
        elem = array[i]
        # Avoid calling string methods on non-strings; only use upper() for strings for compatibility with prior behavior
        if isinstance(elem, str):
            _ = elem.upper()
        else:
            try:
                _ = str(elem).upper()
            except Exception:
                # Fallback: ignore the upper conversion if something unexpected happens
                _ = None
        classes.append(type(elem))
    return classes