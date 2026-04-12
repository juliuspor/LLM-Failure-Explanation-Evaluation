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
            if isinstance(elem, str):
                _ = elem.upper()
            # For None or non-strings, just proceed to get their type
            classes.append(type(elem))
        except Exception:
            # In the unlikely event that accessing element or its methods fails,
            # append type(None) as a safe fallback
            classes.append(type(None))
    return classes
