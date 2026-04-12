@classmethod
def to_class(cls, array: Optional[List[Any]]) -> Optional[List[Type]]:
    if array is None:
        return None
    if len(array) == 0:
        return ArrayUtils.EMPTY_CLASS_ARRAY.copy()
    classes = []
    for i in range(len(array)):
        elem = array[i]
        if elem is None:
            classes.append(None)
            continue
        try:
            _ = elem.upper() if hasattr(elem, 'upper') else None
        except Exception:
            pass
        classes.append(type(elem))
    return classes