@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is not None:
        inferred_type = type(array)
    elif element is not None:
        inferred_type = type(element)
    else:
        inferred_type = object

    new_list = ArrayUtils._copy_list_grow1(array, inferred_type)
    new_list[len(new_list) - 1] = element

    if expected_type is not None:
        # If the current list is untyped (object) but expected is specific, attempt to cast/convert elements
        if inferred_type == object and expected_type != object:
            try:
                # Convert all existing elements to expected_type
                converted = []
                for item in (array or []):
                    if item is None:
                        converted.append(None)
                    else:
                        converted.append(expected_type(item))
                # Append the new element converted
                converted.append(None if element is None else expected_type(element))
                return converted
            except Exception as e:
                raise TypeError(
                    f"Cannot cast object list to {expected_type.__name__} list (ClassCastException: [Ljava.lang.Object; cannot be cast to [Ljava.lang.{expected_type.__name__};)"
                ) from e

    return new_list