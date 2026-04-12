    @staticmethod
    def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
        if array is not None:
            inferred_type = type(array)
        elif element is not None:
            inferred_type = type(element)
        else:
            inferred_type = object

        # Ensure we work with a list (treat None as empty list)
        source = array.copy() if array is not None else []
        # Append a placeholder and set final element
        source.append(None)
        source[len(source) - 1] = element

        # Validate expected_type against the element (not the array)
        if expected_type is not None:
            # If element is not None and is not instance of expected_type, raise
            if element is not None and not isinstance(element, expected_type):
                raise TypeError(
                    f"Cannot cast element of type {type(element).__name__} to {expected_type.__name__} "
                    f"(ClassCastException: {type(element).__name__} cannot be cast to {expected_type.__name__})"
                )
            # If element is None but inferred_type is object and expected_type is more specific, simulate Java-like cast failure
            if element is None and inferred_type == object and expected_type != object:
                raise TypeError(
                    f"Cannot cast object list to {expected_type.__name__} list "
                    f"(ClassCastException: [Ljava.lang.Object; cannot be cast to [Ljava.lang.{expected_type.__name__};)"
                )

        return source