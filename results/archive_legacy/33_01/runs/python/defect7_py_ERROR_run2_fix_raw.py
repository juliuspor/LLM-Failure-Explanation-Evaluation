@classmethod
def to_class(cls, array: Optional[List[Any]]) -> Optional[List[Type]]:
    if array is None:
        return None
    if len(array) == 0:
        return ArrayUtils.EMPTY_CLASS_ARRAY.copy()
    classes: List[Optional[Type]] = []
    for elem in array:
        if elem is None:
            classes.append(None)
            continue
        if isinstance(elem, type):
            classes.append(elem)
            continue
        if isinstance(elem, str):
            try:
                if '.' in elem:
                    module_name, cls_name = elem.rsplit('.', 1)
                    module = __import__(module_name, fromlist=[cls_name])
                    classes.append(getattr(module, cls_name))
                else:
                    classes.append(eval(elem))
            except Exception:
                classes.append(None)
            continue
        try:
            classes.append(type(elem))
        except Exception:
            classes.append(None)
    return classes