@classmethod
def to_class(cls, array: Optional[List[Any]]) -> Optional[List[Type]]:
    if array is None:
        return None
    if len(array) == 0:
        return ArrayUtils.EMPTY_CLASS_ARRAY.copy()
    classes: List[Type] = []
    for elem in array:
        if elem is None:
            classes.append(None)
        elif isinstance(elem, type):
            classes.append(elem)
        else:
            classes.append(type(elem))
    return classes