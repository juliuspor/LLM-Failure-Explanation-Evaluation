@classmethod
def to_class(cls, array: Optional[List[Any]]) -> Optional[List[Type]]:
    if array is None:
        return None
    elif len(array) == 0:
        return ArrayUtils.EMPTY_CLASS_ARRAY.copy()

    classes = []
    for i in range(len(array)):
        el = array[i]
        if el is None:
            classes.append(None)
        else:
            if isinstance(el, str):
                _ = el.upper()
            classes.append(type(el))
    return classes
