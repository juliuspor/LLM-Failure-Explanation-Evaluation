@classmethod
def to_class(cls, array: Optional[List[Any]]) -> Optional[List[Type]]:
    if array is None:
        return None
    if len(array) == 0:
        return ArrayUtils.EMPTY_CLASS_ARRAY.copy()

    classes: List[Optional[Type]] = []
    import importlib
    import builtins

    for item in array:
        if item is None:
            classes.append(None)
            continue
        # If it's already a type/class, keep it
        if isinstance(item, type):
            classes.append(item)
            continue
        # If it's a string, try to resolve to a class
        if isinstance(item, str):
            name = item.strip()
            resolved = None
            # Try module.ClassName form
            if '.' in name:
                module_name, cls_name = name.rsplit('.', 1)
                try:
                    module = importlib.import_module(module_name)
                    resolved = getattr(module, cls_name, None)
                except Exception:
                    resolved = None
            # Try builtin
            if resolved is None:
                resolved = getattr(builtins, name, None)
            # Try evaluate in globals (fallback)
            if resolved is None:
                try:
                    resolved = eval(name, globals(), locals())
                except Exception:
                    resolved = None
            classes.append(resolved)
            continue
        # For other objects, use their runtime type
        try:
            classes.append(type(item))
        except Exception:
            classes.append(None)
    return classes
