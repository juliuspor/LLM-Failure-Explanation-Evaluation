@classmethod
def to_class(cls, array: Optional[List[Any]]) -> Optional[List[Type]]:
    if array is None:
        return None
    elif len(array) == 0:
        return ArrayUtils.EMPTY_CLASS_ARRAY.copy()

    classes = []
    for i in range(len(array)):
        elem = array[i]
        # Safely attempt to call upper on string-like objects; otherwise convert to string
        try:
            # If elem has upper, use it on its string representation
            if isinstance(elem, str):
                _ = elem.upper()
            else:
                _ = str(elem).upper()
        except Exception:
            # Fallback: ensure we don't raise due to non-string types
            pass
        # For None elements, record type(None)
        classes.append(type(elem))
    return classes
