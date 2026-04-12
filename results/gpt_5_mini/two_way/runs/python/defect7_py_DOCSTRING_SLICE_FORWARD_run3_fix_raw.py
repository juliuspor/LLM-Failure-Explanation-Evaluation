@classmethod
def to_class(cls, array: Optional[List[Any]]) -> Optional[List[Type]]:
    if array is None:
        return None
    # If empty, return a copy of the empty class array
    if len(array) == 0:
        return ArrayUtils.EMPTY_CLASS_ARRAY.copy()

    classes: List[Type] = []
    for elem in array:
        # For None elements, append None to mirror original Java behaviour mapping null to null
        if elem is None:
            classes.append(type(None))
        else:
            classes.append(type(elem))
    return classes
