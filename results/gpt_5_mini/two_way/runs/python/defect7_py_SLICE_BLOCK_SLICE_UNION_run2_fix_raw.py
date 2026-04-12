@classmethod
def to_class(cls, array: Optional[List[Any]]) -> Optional[List[Type]]:
    if array is None:
        return None
    elif len(array) == 0:
        return ArrayUtils.EMPTY_CLASS_ARRAY.copy()

    classes = []
    for item in array:
        # Only call .upper() if item is a string; ignore otherwise
        try:
            if isinstance(item, str):
                _ = item.upper()
        except Exception:
            # Ignore any unexpected errors from .upper()
            pass
        # For None, append type(None)
        classes.append(type(item))
    return classes