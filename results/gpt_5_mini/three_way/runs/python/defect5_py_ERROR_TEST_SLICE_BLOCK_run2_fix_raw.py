    @staticmethod
    def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
        if array is not None:
            inferred_type = type(array)
        elif element is not None:
            inferred_type = type(element)
        else:
            inferred_type = object
        # If an expected_type is provided and we only have a generic inferred_type, prefer expected_type
        if expected_type is not None and inferred_type == object and expected_type != object:
            inferred_type = expected_type
        new_list = ArrayUtils._copy_list_grow1(array, inferred_type)
        new_list[len(new_list) - 1] = element
        if expected_type is not None:
            # Only raise if we have a concrete inferred type that is incompatible with expected_type
            if inferred_type is not object and inferred_type != expected_type:
                raise TypeError(
                    f"Cannot cast {inferred_type.__name__} list to {expected_type.__name__} list"
                )
        return new_list