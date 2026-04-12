@classmethod
def to_class(cls, array: Optional[List[Any]]) -> Optional[List[Type]]:
    if array is None:
        return None
    if len(array) == 0:
        return ArrayUtils.EMPTY_CLASS_ARRAY.copy()

    classes: List[Optional[Type]] = []
    for elem in array:
        # None stays None
        if elem is None:
            classes.append(None)
            continue
        # If it's already a type/class, use it
        if isinstance(elem, type):
            classes.append(elem)
            continue
        # If it's a string, try to resolve to a class by name
        if isinstance(elem, str):
            try:
                resolved = cls.get_class(elem)
                classes.append(resolved)
            except Exception:
                classes.append(None)
            continue
        # For any other object, use its runtime type
        try:
            classes.append(type(elem))
        except Exception:
            classes.append(None)
    return classes