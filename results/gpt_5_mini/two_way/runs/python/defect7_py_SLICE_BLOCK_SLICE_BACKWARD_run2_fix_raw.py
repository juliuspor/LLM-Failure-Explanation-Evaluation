@classmethod
def to_class(cls, array: Optional[List[Any]]) -> Optional[List[Type]]:
    if array is None:
        return None
    elif len(array) == 0:
        return ArrayUtils.EMPTY_CLASS_ARRAY.copy()

    classes = []
    for i in range(len(array)):
        elem = array[i]
        try:
            # Safely obtain an uppercased string representation if needed
            if isinstance(elem, str):
                _ = elem.upper()
            else:
                _ = str(elem).upper()
        except Exception:
            # Fallback: skip the upper call but proceed to record the type
            pass
        classes.append(type(elem))
    return classes
