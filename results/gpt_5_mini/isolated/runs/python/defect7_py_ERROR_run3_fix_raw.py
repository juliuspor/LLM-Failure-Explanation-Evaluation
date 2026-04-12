@classmethod
def to_class(cls, array: Optional[List[Any]]) -> Optional[List[Type]]:
    if array is None:
        return None
    elif len(array) == 0:
        return ArrayUtils.EMPTY_CLASS_ARRAY.copy()

    classes: List[Type] = []
    for item in array:
        # If the item itself is None, preserve None in the resulting list
        if item is None:
            classes.append(type(None))
            continue
        # If the item is already a type, use it directly
        if isinstance(item, type):
            classes.append(item)
            continue
        # Otherwise get the runtime type of the object
        classes.append(type(item))
    return classes