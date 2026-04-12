@classmethod
def to_class(cls, array: Optional[List[Any]]) -> Optional[List[Type]]:
    if array is None:
        return None
    elif len(array) == 0:
        return ArrayUtils.EMPTY_CLASS_ARRAY.copy()

    classes: List[Type] = []
    for i, val in enumerate(array):
        try:
            if isinstance(val, str):
                _ = val.upper()
            # Always append the actual type (None -> type(None))
            classes.append(type(val))
        except AttributeError:
            # Fallback: convert to string for debugging but still append type
            try:
                _ = str(val).upper()
            except Exception:
                # If even str(val) fails, re-raise with context
                raise
            classes.append(type(val))
    return classes