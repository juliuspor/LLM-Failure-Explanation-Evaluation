@classmethod
def to_class(cls, array: Optional[List[Any]]) -> Optional[List[Type]]:
    if array is None:
        return None
    elif len(array) == 0:
        return ArrayUtils.EMPTY_CLASS_ARRAY.copy()

    classes: List[Type] = []
    for elem in array:
        if elem is None:
            classes.append(None)
        elif isinstance(elem, str):
            try:
                resolved = cls.get_class(elem)
                classes.append(resolved)
            except Exception:
                # If string cannot be resolved to a class, treat it as the type of the string value
                classes.append(type(elem))
        elif isinstance(elem, type):
            classes.append(elem)
        else:
            classes.append(type(elem))
    return classes