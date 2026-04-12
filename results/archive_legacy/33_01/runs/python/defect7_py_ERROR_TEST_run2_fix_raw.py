@classmethod
def to_class(cls, array: Optional[List[Any]]) -> Optional[List[Type]]:
    if array is None:
        return None
    elif len(array) == 0:
        return ArrayUtils.EMPTY_CLASS_ARRAY.copy()
    classes = []
    for i in range(len(array)):
        value = array[i]
        if value is None:
            classes.append(type(None))
            continue
        if isinstance(value, str):
            name = StringUtils.delete_whitespace(value)
            try:
                if '.' in name:
                    module_name, cls_name = name.rsplit('.', 1)
                    module = __import__(module_name, fromlist=[cls_name])
                    classes.append(getattr(module, cls_name))
                else:
                    classes.append(eval(name))
            except Exception:
                classes.append(None)
        else:
            classes.append(type(value))
    return classes