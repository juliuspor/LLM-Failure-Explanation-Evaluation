    @classmethod
    def get_class(cls, class_name: str, initialize: bool = True) -> Type:
        """
        Returns the class represented by class_name using the
        current module context. This implementation supports names like
        "module.ClassName" as well as built-in type names.
        
        Args:
            class_name: the class name
            initialize: whether the class must be initialized (not used in Python)
            
        Returns:
            the class represented by class_name
            
        Raises:
            ImportError: if the class is not found
        """
        class_name = cls._to_canonical(class_name)
        
        # Handle primitive type abbreviations
        primitive_map = {
            'boolean': bool,
            'byte': int,
            'char': str,
            'short': int,
            'int': int,
            'long': int,
            'float': float,
            'double': float,
            'void': type(None)
        }
        if class_name in primitive_map:
            return primitive_map[class_name]
        
        # Try to import module and get class
        if '.' in class_name:
            module_name, cls_name = class_name.rsplit('.', 1)
            try:
                module = __import__(module_name, fromlist=[cls_name])
                return getattr(module, cls_name)
            except (ImportError, AttributeError):
                pass
        
        # Try built-ins
        try:
            return eval(class_name)
        except NameError:
            raise ImportError(f"Class '{class_name}' not found")