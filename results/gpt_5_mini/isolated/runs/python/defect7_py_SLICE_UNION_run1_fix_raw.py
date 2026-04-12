@classmethod
def to_class(cls, array: Optional[List[Any]]) -> Optional[List[Type]]:
    if array is None:
        return None
    elif len(array) == 0:
        return ArrayUtils.EMPTY_CLASS_ARRAY.copy()

    classes = []
    for i in range(len(array)):
        element = array[i]
        # Only call upper() if element is a string; otherwise, safely skip or convert to string
        if isinstance(element, str):
            _ = element.upper()
        else:
            # Ensure we don't attempt to call upper() on non-string types
            _ = None
        classes.append(type(element))
    return classes
