@classmethod
def to_class(cls, array: Optional[List[Any]]) -> Optional[List[Type]]:
    if array is None:
        return None
    elif len(array) == 0:
        return ArrayUtils.EMPTY_CLASS_ARRAY.copy()

    classes = []
    for i in range(len(array)):
        elem = array[i]
        # Only call upper on strings; ignore otherwise
        if isinstance(elem, str):
            try:
                _ = elem.upper()
            except Exception:
                # If upper unexpectedly fails, continue but record the type
                pass
        classes.append(type(elem))
    return classes