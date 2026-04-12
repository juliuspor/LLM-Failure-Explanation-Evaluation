@staticmethod
    def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
        if expected_type is not None:
            inferred_component_type = expected_type
        else:
            # Infer from first non-None element in array, else from element, else object
            inferred_component_type = object
            if array is not None:
                for item in array:
                    if item is not None:
                        inferred_component_type = type(item)
                        break
            if inferred_component_type is object and element is not None:
                inferred_component_type = type(element)

        new_list = ArrayUtils._copy_list_grow1(array, inferred_component_type)
        new_list[len(new_list) - 1] = element

        # If expected_type provided, simulate Java-like ClassCastException when types incompatible
        if expected_type is not None:
            # If we couldn't determine a concrete component type (object) but expected is more specific, raise
            if inferred_component_type is object and expected_type is not object:
                raise TypeError(
                    f"Cannot cast object list to {expected_type.__name__} list "
                    f"(ClassCastException: [Ljava.lang.Object; cannot be cast to [Ljava.lang.{expected_type.__name__};)"
                )
        return new_list