@classmethod
def to_class(cls, array: Optional[List[Any]]) -> Optional[List[Type]]:
    if array is None:
        return None
    elif len(array) == 0:
        return ArrayUtils.EMPTY_CLASS_ARRAY.copy()

    classes = []
    for i in range(len(array)):
        element = array[i]
        # If element is a string and normalization is needed, apply it safely
        if isinstance(element, str):
            _ = element.upper()
        classes.append(type(element))
    return classes
