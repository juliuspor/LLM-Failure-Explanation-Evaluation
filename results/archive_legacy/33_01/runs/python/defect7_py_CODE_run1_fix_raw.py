@classmethod
def to_class(cls, array: Optional[List[Any]]) -> Optional[List[Type]]:
    if array is None:
        return None
    if len(array) == 0:
        return ArrayUtils.EMPTY_CLASS_ARRAY.copy()
    classes = []
    for item in array:
        if item is None:
            classes.append(None)
            continue
        if isinstance(item, type):
            classes.append(item)
            continue
        if isinstance(item, str):
            name = item.strip()
            try:
                if '.' in name:
                    module_name, cls_name = name.rsplit('.', 1)
                    module = __import__(module_name, fromlist=[cls_name])
                    classes.append(getattr(module, cls_name))
                else:
                    try:
                        classes.append(getattr(sys.modules.get('__builtin__', sys.modules.get('builtins')), name))
                    except Exception:
                        try:
                            classes.append(eval(name))
                        except Exception:
                            classes.append(None)
            except Exception:
                classes.append(None)
            continue
        try:
            classes.append(type(item))
        except Exception:
            classes.append(None)
    return classes