@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None and len(array) > 0:
        component_type = type(array[0])
    elif element is not None:
        component_type = type(element)
    elif expected_type is not None:
        component_type = expected_type
    else:
        component_type = object

    new_list = ArrayUtils._copy_list_grow1(array, component_type)
    new_list[len(new_list) - 1] = element

    if expected_type is not None:
        try:
            if isinstance(component_type, type):
                if not issubclass(component_type, expected_type) and component_type is not expected_type:
                    raise TypeError(
                        f"Cannot cast object list to {expected_type.__name__} list "
                        f"(ClassCastException: [Ljava.lang.Object; cannot be cast to "
                        f"[Ljava.lang.{expected_type.__name__};)"
                    )
        except TypeError:
            raise
        except Exception:
            pass

    return new_list