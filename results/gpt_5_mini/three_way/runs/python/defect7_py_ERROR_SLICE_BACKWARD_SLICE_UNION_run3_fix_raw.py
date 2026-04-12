@classmethod
def to_class(cls, array: Optional[List[Any]]) -> Optional[List[Type]]:
    if array is None:
        return None
    elif len(array) == 0:
        return ArrayUtils.EMPTY_CLASS_ARRAY.copy()

    classes = []
    for i, elem in enumerate(array):
        try:
            if elem is None:
                classes.append(None)
                continue
            # Only call upper on strings; coerce others to string first
            if not isinstance(elem, str):
                val = str(elem)
            else:
                val = elem
            _ = val.upper()
        except Exception:
            # On unexpected error, append the type if possible, otherwise None
            try:
                classes.append(type(elem))
            except Exception:
                classes.append(None)
        else:
            classes.append(type(elem))
    return classes