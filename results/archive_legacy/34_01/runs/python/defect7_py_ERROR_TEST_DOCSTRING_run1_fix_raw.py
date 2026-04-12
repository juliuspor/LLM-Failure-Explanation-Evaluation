@classmethod
def to_class(cls, array: Optional[List[Any]]) -> Optional[List[Type]]:
    if array is None:
        return None
    if len(array) == 0:
        return ArrayUtils.EMPTY_CLASS_ARRAY.copy()
    classes: List[Type] = []
    for el in array:
        if el is None:
            classes.append(None)
            continue
        if isinstance(el, type):
            classes.append(el)
            continue
        if isinstance(el, str):
            name = StringUtils.delete_whitespace(el)
            if name is None or len(name) == 0:
                classes.append(None)
                continue
            try:
                if '.' in name:
                    module_name, cls_name = name.rsplit('.', 1)
                    module = __import__(module_name, fromlist=[cls_name])
                    classes.append(getattr(module, cls_name))
                else:
                    try:
                        classes.append(eval(name))
                    except Exception:
                        classes.append(None)
            except Exception:
                classes.append(None)
            continue
        classes.append(type(el))
    return classes