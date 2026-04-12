@classmethod
def to_class(cls, array: Optional[List[Any]]) -> Optional[List[Type]]:
    if array is None:
        return None
    elif len(array) == 0:
        return ArrayUtils.EMPTY_CLASS_ARRAY.copy()

    classes = []
    for i in range(len(array)):
        element = array[i]
        # Handle None elements explicitly: preserve None as in original convert methods
        if element is None:
            classes.append(None)
            continue
        # If element is a string and was intended to be upper-cased previously, avoid calling upper() on non-strings.
        # The original .upper() call had no effect on type determination, so we simply determine the type safely.
        classes.append(type(element))
    return classes
