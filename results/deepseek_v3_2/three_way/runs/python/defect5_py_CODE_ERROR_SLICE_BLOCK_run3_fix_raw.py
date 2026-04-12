    @staticmethod
    def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
        if array is not None:
            new_list = array.copy()
            new_list.append(element)
            return new_list
        else:
            new_list = []
            if element is not None:
                new_list.append(element)
            else:
                new_list.append(None)
            if expected_type is not None:
                inferred_type = object if element is None else type(element)
                if inferred_type == object and expected_type != object:
                    raise TypeError(
                        f"Cannot cast object list to {expected_type.__name__} list "
                        f"(ClassCastException: [Ljava.lang.Object; cannot be cast to "
                        f"[Ljava.lang.{expected_type.__name__};)"
                    )
            return new_list