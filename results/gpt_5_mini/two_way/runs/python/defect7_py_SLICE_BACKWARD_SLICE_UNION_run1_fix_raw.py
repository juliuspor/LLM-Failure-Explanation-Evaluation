@classmethod
def to_class(cls, array: Optional[List[Any]]) -> Optional[List[Type]]:
    if array is None:
        return None
    elif len(array) == 0:
        return ArrayUtils.EMPTY_CLASS_ARRAY.copy()

    classes: List[Type] = []
    for elem in array:
        # Safely handle strings by uppercasing if necessary; do not call upper() on non-strings
        if isinstance(elem, str):
            _ = elem.upper()
            classes.append(type(elem))
        else:
            # For None, use type(None); for other objects, use their type
            classes.append(type(elem))
    return classes