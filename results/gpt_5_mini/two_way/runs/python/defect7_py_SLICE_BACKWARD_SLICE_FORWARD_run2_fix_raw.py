@classmethod
def to_class(cls, array: Optional[List[Any]]) -> Optional[List[Type]]:
    if array is None:
        return None
    elif len(array) == 0:
        return ArrayUtils.EMPTY_CLASS_ARRAY.copy()

    classes = []
    for i in range(len(array)):
        elem = array[i]
        # Preserve original behavior: return the type of the element.
        # Handle None explicitly (type(None)) and other non-string types without attempting string ops.
        classes.append(type(elem))
    return classes
