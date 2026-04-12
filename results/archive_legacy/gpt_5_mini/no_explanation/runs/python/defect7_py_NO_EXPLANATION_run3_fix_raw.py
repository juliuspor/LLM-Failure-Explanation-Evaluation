@classmethod
def to_class(cls, array: Optional[List[Any]]) -> Optional[List[Type]]:
    if array is None:
        return None
    if len(array) == 0:
        return ArrayUtils.EMPTY_CLASS_ARRAY.copy()

    classes: List[Type] = []
    for elem in array:
        if elem is None:
            classes.append(None)
            continue
        # If already a class/type, use it directly
        if isinstance(elem, type):
            classes.append(elem)
            continue
        # If a string, attempt to resolve to a class name
        if isinstance(elem, str):
            try:
                resolved = cls.get_class(elem)
                classes.append(resolved)
                continue
            except Exception:
                # Fall back to using the string object's type
                classes.append(type(elem))
                continue
        # Fallback: return the runtime type of the object
        classes.append(type(elem))
    return classes
