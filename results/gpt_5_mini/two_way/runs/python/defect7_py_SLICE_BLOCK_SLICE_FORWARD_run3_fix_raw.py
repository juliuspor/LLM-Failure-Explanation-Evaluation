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
            else:
                # If not a string, avoid calling string methods
                pass
        except Exception:
            # Defensive: ignore issues with upper() and continue
            pass
        classes.append(type(elem))
    return classes
