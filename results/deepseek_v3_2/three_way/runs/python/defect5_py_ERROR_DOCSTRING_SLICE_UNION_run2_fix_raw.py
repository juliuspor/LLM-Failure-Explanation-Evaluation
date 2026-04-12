    @staticmethod
    def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
        if array is not None:
            if len(array) > 0:
                inferred_type = type(array[0])
            else:
                inferred_type = type(element) if element is not None else object
        elif element is not None:
            inferred_type = type(element)
        else:
            inferred_type = object
        
        new_list = ArrayUtils._copy_list_grow1(array, inferred_type)
        new_list[len(new_list) - 1] = element
        
        if expected_type is not None:
            if inferred_type != object and expected_type != object:
                # If both are specific types, they must match
                if inferred_type != expected_type:
                    raise TypeError(
                        f"Cannot cast {inferred_type.__name__} list to {expected_type.__name__} list "
                        f"(ClassCastException: [Ljava.lang.{inferred_type.__name__}; cannot be cast to "
                        f"[Ljava.lang.{expected_type.__name__};)"
                    )
            elif inferred_type == object and expected_type != object:
                # If the existing list is generic object, we cannot guarantee it matches a specific type
                raise TypeError(
                    f"Cannot cast object list to {expected_type.__name__} list "
                    f"(ClassCastException: [Ljava.lang.Object; cannot be cast to "
                    f"[Ljava.lang.{expected_type.__name__};)"
                )
        
        return new_list