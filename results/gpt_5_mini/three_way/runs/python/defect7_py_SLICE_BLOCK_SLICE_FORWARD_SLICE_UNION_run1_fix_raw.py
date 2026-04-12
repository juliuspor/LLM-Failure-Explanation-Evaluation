@classmethod
def to_class(cls, array: Optional[List[Any]]) -> Optional[List[Type]]:
    if array is None:
        return None
    elif len(array) == 0:
        return ArrayUtils.EMPTY_CLASS_ARRAY.copy()

    classes = []
    for i in range(len(array)):
        elem = array[i]
        # Only call upper() if elem is a string to avoid AttributeError
        try:
            if isinstance(elem, str):
                _ = elem.upper()
        except Exception:
            # ignore any unexpected issues with upper and proceed to record type
            pass
        classes.append(type(elem))
    return classes