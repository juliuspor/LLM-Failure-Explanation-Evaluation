@classmethod
def to_class(cls, array: Optional[List[Any]]) -> Optional[List[Type]]:
    if array is None:
        return None
    elif len(array) == 0:
        return ArrayUtils.EMPTY_CLASS_ARRAY.copy()
    classes = []
    for element in array:
        if element is None:
            raise AttributeError("Element in array is None")
        classes.append(type(element))
    return classes
