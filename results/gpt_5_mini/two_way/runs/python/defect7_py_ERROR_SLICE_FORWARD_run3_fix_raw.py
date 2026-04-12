@classmethod
def to_class(cls, array: Optional[List[Any]]) -> Optional[List[Type]]:
    if array is None:
        return None
    elif len(array) == 0:
        return ArrayUtils.EMPTY_CLASS_ARRAY.copy()

    classes = []
    for i in range(len(array)):
        val = array[i]
        # Safely attempt to call upper() only if val is not None and has upper
        if val is None:
            classes.append(None)
        else:
            try:
                if hasattr(val, 'upper') and callable(getattr(val, 'upper')):
                    _ = val.upper()
            except Exception:
                # Ignore any errors from upper()
                pass
            classes.append(type(val))
    return classes
