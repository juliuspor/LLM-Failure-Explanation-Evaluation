    @staticmethod
    def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
        if array is not None:
            inferred_type = type(array)
        elif expected_type is not None:
            # Use expected_type when array is None to simulate Java component type
            inferred_type = expected_type
        elif element is not None:
            inferred_type = type(element)
        else:
            inferred_type = object

        # If expected_type provided, ensure compatibility with element when present
        if expected_type is not None and element is not None:
            if not isinstance(element, expected_type):
                raise TypeError(
                    f"Cannot cast element of type {type(element).__name__} to {expected_type.__name__}"
                )

        new_list = ArrayUtils._copy_list_grow1(array, inferred_type)
        new_list[len(new_list) - 1] = element

        if expected_type is not None:
            # Simulate Java cast failure if we inferred a generic object list but expected a specific type
            if inferred_type == object and expected_type != object:
                raise TypeError(
                    f"Cannot cast object list to {expected_type.__name__} list "
                    f"(ClassCastException: [Ljava.lang.Object; cannot be cast to "
                    f"[Ljava.lang.{expected_type.__name__};)"
                )

        return new_list