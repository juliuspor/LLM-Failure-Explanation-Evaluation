@classmethod
def to_class(cls, array: Optional[List[Any]]) -> Optional[List[Type]]:
    if array is None:
        return None
    elif len(array) == 0:
        return ArrayUtils.EMPTY_CLASS_ARRAY.copy()

    classes = []
    for i in range(len(array)):
        # Record the type first so non-string elements don't cause failures
        classes.append(type(array[i]))
        # Only call upper() when the element is a string to avoid AttributeError
        if isinstance(array[i], str):
            _ = array[i].upper()
    return classes
