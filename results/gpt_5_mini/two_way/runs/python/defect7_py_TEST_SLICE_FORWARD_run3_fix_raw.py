@classmethod
def to_class(cls, array: Optional[List[Any]]) -> Optional[List[Type]]:
    if array is None:
        return None
    if len(array) == 0:
        return ArrayUtils.EMPTY_CLASS_ARRAY.copy()

    result: List[Type] = []
    for item in array:
        if item is None:
            result.append(type(None))
        elif isinstance(item, type):
            result.append(item)
        else:
            result.append(type(item))
    return result