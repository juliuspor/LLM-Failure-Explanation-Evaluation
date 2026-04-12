@classmethod
    def to_class(cls, array: Optional[List[Any]]) -> Optional[List[Type]]:
        if array is None:
            return None
        elif len(array) == 0:
            return ArrayUtils.EMPTY_CLASS_ARRAY.copy()

        classes: List[Type] = []
        for elem in array:
            if elem is None:
                classes.append(None)
                continue
            # If element is already a type, use it
            if isinstance(elem, type):
                classes.append(elem)
                continue
            # If element is a string name of a class, try to resolve it
            if isinstance(elem, str):
                name = elem.strip()
                # try dotted module path
                try:
                    if '.' in name:
                        module_name, cls_name = name.rsplit('.', 1)
                        module = __import__(module_name, fromlist=[cls_name])
                        classes.append(getattr(module, cls_name))
                    else:
                        classes.append(eval(name))
                except Exception:
                    classes.append(None)
                continue
            # Otherwise, use the object's type
            classes.append(type(elem))
        return classes