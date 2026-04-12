@classmethod
def to_class(cls, array: Optional[List[Any]]) -> Optional[List[Type]]:
    if array is None:
        return None
    if len(array) == 0:
        return ArrayUtils.EMPTY_CLASS_ARRAY.copy()
    classes = []
    for v in array:
        if v is None:
            classes.append(None)
            continue
        if isinstance(v, type):
            classes.append(v)
            continue
        if isinstance(v, str):
            try:
                resolved = cls.get_class(v)
            except Exception:
                try:
                    resolved = eval(v)
                except Exception:
                    resolved = None
            classes.append(resolved)
            continue
        classes.append(type(v))
    return classes