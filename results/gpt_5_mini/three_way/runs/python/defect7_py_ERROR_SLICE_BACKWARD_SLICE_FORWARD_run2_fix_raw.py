@classmethod
def to_class(cls, array: Optional[List[Any]]) -> Optional[List[Type]]:
    if array is None:
        return None
    elif len(array) == 0:
        return ArrayUtils.EMPTY_CLASS_ARRAY.copy()

    classes = []
    for i in range(len(array)):
        element = array[i]
        if element is None:
            classes.append(None)
            continue
        # If element is a string name of a class, try to resolve it to a class
        if isinstance(element, str):
            try:
                resolved = cls.get_class(element)
                classes.append(resolved)
            except Exception:
                # If resolution fails, fall back to the string's type
                classes.append(type(element))
        else:
            classes.append(type(element))
    return classes