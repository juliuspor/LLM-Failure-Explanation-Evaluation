    @staticmethod
    def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
        if array is None:
            # infer element type from element if possible
            if element is not None:
                inferred_element_type = type(element)
            else:
                inferred_element_type = expected_type if expected_type is not None else object
        else:
            # try to infer element type from existing elements in the list
            inferred_element_type = None
            for item in array:
                if item is not None:
                    inferred_element_type = type(item)
                    break
            if inferred_element_type is None:
                # no non-None elements in array
                if element is not None:
                    inferred_element_type = type(element)
                else:
                    inferred_element_type = expected_type if expected_type is not None else object

        new_list = ArrayUtils._copy_list_grow1(array, inferred_element_type)
        new_list[len(new_list) - 1] = element

        if expected_type is not None:
            # only simulate a class cast failure when we truly don't know element type (object)
            if inferred_element_type is object and expected_type is not object:
                raise TypeError(
                    f"Cannot cast object list to {expected_type.__name__} list "
                    f"(ClassCastException: [Ljava.lang.Object; cannot be cast to "
                    f"[Ljava.lang.{expected_type.__name__};)"
                )
        return new_list