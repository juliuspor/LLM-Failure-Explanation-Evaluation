@classmethod
def to_class(cls, array: Optional[List[Any]]) -> Optional[List[Type]]:
    if array is None:
        return None
    if len(array) == 0:
        return list(ArrayUtils.EMPTY_CLASS_ARRAY)
    classes: List[Type] = []
    for element in array:
        if element is None:
            classes.append(None)
        elif isinstance(element, type):
            classes.append(element)
        else:
            classes.append(type(element))
    return classes