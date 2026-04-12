@classmethod
def to_class(cls, array: Optional[List[Any]]) -> Optional[List[Type]]:
    if array is None:
        return None
    elif len(array) == 0:
        return ArrayUtils.EMPTY_CLASS_ARRAY.copy()

    classes = []
    for element in array:
        # Safely handle non-string elements when uppercasing was intended for normalization
        try:
            _ = None if element is None else str(element).upper()
        except Exception:
            # If conversion/upper fails for some unusual object, skip normalization
            _ = None
        classes.append(type(element))
    return classes
