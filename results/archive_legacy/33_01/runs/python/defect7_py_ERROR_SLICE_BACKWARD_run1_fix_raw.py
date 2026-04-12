@classmethod
def to_class(cls, array: Optional[List[Any]]) -> Optional[List[Type]]:
    if array is None:
        return None
    if len(array) == 0:
        return ArrayUtils.EMPTY_CLASS_ARRAY.copy()
    classes: List[Optional[Type]] = []
    for i, elem in enumerate(array):
        if elem is None:
            classes.append(None)
            continue
        if isinstance(elem, type):
            classes.append(elem)
            continue
        try:
            if isinstance(elem, str):
                classes.append(cls.get_class(elem))
            else:
                classes.append(type(elem))
        except Exception:
            try:
                classes.append(type(elem))
            except Exception:
                classes.append(None)
    return classes