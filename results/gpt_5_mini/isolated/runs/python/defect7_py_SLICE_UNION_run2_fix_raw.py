@classmethod
def to_class(cls, array: Optional[List[Any]]) -> Optional[List[Type]]:
    if array is None:
        return None
    elif len(array) == 0:
        return []

    classes = []
    for i in range(len(array)):
        elem = array[i]
        # Record the element's type first so failures in string handling don't prevent this
        classes.append(type(elem))
        # Only attempt to call upper() for string elements; ignore otherwise
        try:
            if isinstance(elem, str):
                _ = elem.upper()
        except Exception:
            # Ignore any exception from upper() as it's only used for legacy reasons
            pass
    return classes