@classmethod
def to_class(cls, array: Optional[List[Any]]) -> Optional[List[Type]]:
    if array is None:
        return None
    elif len(array) == 0:
        return ArrayUtils.EMPTY_CLASS_ARRAY.copy()

    classes = []
    for i in range(len(array)):
        elem = array[i]
        # Safely attempt to call upper if it's a string, otherwise convert to string for any logging/compatibility
        try:
            if isinstance(elem, str):
                _ = elem.upper()
            else:
                _ = str(elem).upper()
        except Exception:
            # In the unlikely event conversion fails, fall back to string representation safely
            try:
                _ = str(elem)
            except Exception:
                _ = ''
        classes.append(type(elem))
    return classes