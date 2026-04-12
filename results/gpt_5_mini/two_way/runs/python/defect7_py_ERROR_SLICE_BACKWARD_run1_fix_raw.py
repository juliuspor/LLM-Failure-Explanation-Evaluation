@classmethod
    def to_class(cls, array: Optional[List[Any]]) -> Optional[List[Type]]:
        if array is None:
            return None
        if len(array) == 0:
            return ArrayUtils.EMPTY_CLASS_ARRAY.copy()

        classes: List[Type] = []
        for item in array:
            # Only attempt string operations if item is a string
            if isinstance(item, str):
                # preserve original string case for type lookup, but if caller
                # intended upper-case conversion, do it safely
                s = item.upper()
                try:
                    # try to evaluate built-in type name or import
                    if '.' in s:
                        module_name, cls_name = s.rsplit('.', 1)
                        module = __import__(module_name, fromlist=[cls_name])
                        resolved = getattr(module, cls_name)
                    else:
                        resolved = eval(s)
                except Exception:
                    # fallback to type of original string object
                    resolved = type(item)
                classes.append(resolved)
            elif item is None:
                classes.append(type(None))
            else:
                classes.append(type(item))
        return classes