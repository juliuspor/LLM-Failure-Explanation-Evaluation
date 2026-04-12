    @staticmethod
    def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
        if array is not None:
            inferred_type = type(array)
        elif element is not None:
            inferred_type = type(element)
        else:
            inferred_type = None  # No type can be inferred
        
        new_list = ArrayUtils._copy_list_grow1(array, inferred_type)
        new_list[len(new_list) - 1] = element
        
        if expected_type is not None:
            if inferred_type is not None and inferred_type != object and expected_type != object:
                # Simulate type checking only if we have a concrete inferred type
                # and it's not object (i.e., a specific type list)
                # In Python, we cannot enforce this strictly, so we just pass.
                pass
            # If inferred_type is None (both array and element are None), we cannot do any type check.
            # If inferred_type is object, we also skip the check because object list can hold any type.
        
        return new_list