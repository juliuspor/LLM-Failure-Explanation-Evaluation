    @staticmethod
    def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
        if array is not None:
            # infer element type from the array contents (first non-None element)
            inferred_element_type = None
            for item in array:
                if item is not None:
                    inferred_element_type = type(item)
                    break
            if inferred_element_type is None:
                # fallback: if array has __orig_class__ info or use list type as last resort
                inferred_element_type = object
        elif element is not None:
            inferred_element_type = type(element)
        else:
            inferred_element_type = object

        new_list = ArrayUtils._copy_list_grow1(array, inferred_element_type)
        new_list[len(new_list) - 1] = element

        if expected_type is not None:
            # Only raise if we have definite information that element type is object
            # while expected_type is more specific. If we inferred a concrete type,
            # allow the operation (Python is dynamically typed) but if it conflicts
            # with expected_type and element is not None, raise.
            if inferred_element_type == object and expected_type != object:
                raise TypeError(
                    f"Cannot cast object list to {expected_type.__name__} list "
                    f"(ClassCastException: [Ljava.lang.Object; cannot be cast to "
                    f"[Ljava.lang.{expected_type.__name__};)"
                )
            if inferred_element_type is not object and element is not None and not issubclass(inferred_element_type, expected_type):
                raise TypeError(
                    f"Cannot cast list element type {inferred_element_type.__name__} to {expected_type.__name__}"
                )

        return new_list