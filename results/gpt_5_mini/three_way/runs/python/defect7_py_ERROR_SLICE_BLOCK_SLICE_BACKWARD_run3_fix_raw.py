@classmethod
def to_class(cls, array: Optional[List[Any]]) -> Optional[List[Type]]:
    if array is None:
        return None
    elif len(array) == 0:
        return ArrayUtils.EMPTY_CLASS_ARRAY.copy()

    classes = []
    for i in range(len(array)):
        elem = array[i]
        # Only call upper on strings; handle None and other types safely
        if elem is None:
            classes.append(None)
        else:
            # If it's a string, the original code attempted to upper() it for unknown reason;
            # we do not need to modify the element to determine its type. Just append its type.
            try:
                classes.append(type(elem))
            except Exception:
                # Fallback in unexpected cases
                classes.append(None)
    return classes