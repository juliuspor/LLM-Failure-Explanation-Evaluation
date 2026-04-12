@classmethod
def to_class(cls, array: Optional[List[Any]]) -> Optional[List[Type]]:
    if array is None:
        return None
    if len(array) == 0:
        return list(ArrayUtils.EMPTY_CLASS_ARRAY)
    return [type(elem) for elem in array]