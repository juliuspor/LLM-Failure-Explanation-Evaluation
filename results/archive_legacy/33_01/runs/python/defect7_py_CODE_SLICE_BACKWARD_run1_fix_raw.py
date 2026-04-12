@classmethod
def to_class(cls, array: Optional[List[Any]]) -> Optional[List[Type]]:
    if array is None:
        return None
    if len(array) == 0:
        return ArrayUtils.EMPTY_CLASS_ARRAY.copy()
    classes: List[Optional[Type]] = []
    for el in array:
        if el is None:
            classes.append(None)
            continue
        if isinstance(el, type):
            classes.append(el)
            continue
        if isinstance(el, str):
            try:
                resolved = cls.get_class(el)
            except Exception:
                resolved = None
            classes.append(resolved)
            continue
        classes.append(type(el))
    return classes