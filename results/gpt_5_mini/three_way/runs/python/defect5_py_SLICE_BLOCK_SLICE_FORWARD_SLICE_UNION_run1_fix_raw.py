    @staticmethod
    def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
        if array is not None and len(array) > 0:
            inferred_type = type(array[0])
        elif element is not None:
            inferred_type = type(element)
        else:
            inferred_type = object

        new_list = ArrayUtils._copy_list_grow1(array, inferred_type)
        new_list[len(new_list) - 1] = element

        if expected_type is not None:
            # If we have concrete elements, ensure they are instances of expected_type
            # Check existing elements (if any) and the newly added element
            to_check = []
            if array is not None:
                to_check.extend([e for e in array if e is not None])
            if element is not None:
                to_check.append(element)

            for e in to_check:
                if not isinstance(e, expected_type):
                    raise TypeError(
                        f"Element of type {type(e).__name__} cannot be cast to {expected_type.__name__}"
                    )

        return new_list