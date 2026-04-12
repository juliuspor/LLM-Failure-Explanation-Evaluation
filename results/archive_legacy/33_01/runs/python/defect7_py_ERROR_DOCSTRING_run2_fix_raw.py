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
        if isinstance(elem, type):
            classes.append(elem)
            continue
        if isinstance(elem, str):
            try:
                classes.append(cls.get_class(elem))
            except Exception:
                classes.append(None)
            continue
        try:
            classes.append(type(elem))
        except Exception:
            classes.append(None)
    return classes