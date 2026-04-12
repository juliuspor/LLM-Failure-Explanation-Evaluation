@classmethod
def to_class(cls, array: Optional[List[Any]]) -> Optional[List[Type]]:
    if array is None:
        return None
    elif len(array) == 0:
        return ArrayUtils.EMPTY_CLASS_ARRAY.copy()

    classes = []
    for i in range(len(array)):
        element = array[i]
        try:
            if isinstance(element, str):
                _ = element.upper()
        except Exception:
            # Ignore unexpected errors from upper(); proceed to record the type
            pass
        # For None, use type(None)
        classes.append(type(element))
    return classes
