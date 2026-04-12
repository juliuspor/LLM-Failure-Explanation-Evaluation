@classmethod
def to_class(cls, array: Optional[List[Any]]) -> Optional[List[Type]]:
    if array is None:
        return None
    elif len(array) == 0:
        return ArrayUtils.EMPTY_CLASS_ARRAY.copy()

    classes = []
    for item in array:
        # Safely attempt to call upper() only on strings; otherwise obtain string rep
        try:
            if isinstance(item, str):
                _ = item.upper()
            else:
                # ensure non-strings don't cause AttributeError
                _ = str(item).upper()
        except Exception:
            # In case upper or str unexpectedly fail, ignore and proceed
            pass
        classes.append(type(item))
    return classes