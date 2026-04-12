    @classmethod
    def to_locale(cls, locale_str: str) -> Optional[Locale]:
        """
        Parse a locale string into a `Locale` object.

        This translation follows the underscore-separated forms used by the
        Java implementation and validates casing and separators.

        Examples:
            LocaleUtils.to_locale("en")        -> Locale("en", "")
            LocaleUtils.to_locale("en_GB")     -> Locale("en", "GB")
            LocaleUtils.to_locale("en_GB_xxx") -> Locale("en", "GB", "xxx")

        Args:
            locale_str: Locale string to convert. If None, returns None.
            
        Returns:
            A `Locale` instance, or None if `locale_str` is None.
            
        Raises:
            ValueError: If `locale_str` does not match the expected format.
        """
        if locale_str is None:
            return None
        
        # Split by underscore, but handle consecutive underscores as empty segments
        parts = locale_str.split('_')
        
        # Validate at least one part exists
        if not parts:
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        language = parts[0]
        country = ""
        variant = ""
        
        # Validate language: must be 2 or 3 letters, all lowercase
        if not language or not language.isalpha() or not language.islower():
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        if len(parts) >= 2:
            country_part = parts[1]
            # Country can be empty (like in "fr__POSIX") or 2 letters/3 digits
            if country_part:
                # Validate country: must be 2 letters uppercase or 3 digits
                if len(country_part) == 2 and country_part.isalpha() and country_part.isupper():
                    country = country_part
                elif len(country_part) == 3 and country_part.isdigit():
                    country = country_part
                else:
                    raise ValueError(f"Invalid locale format: {locale_str}")
            # If country_part is empty, country remains empty string
            
        if len(parts) >= 3:
            # Variant is everything after the second underscore, joined by underscores
            # to preserve any internal underscores in the variant
            variant_parts = parts[2:]
            variant = '_'.join(variant_parts)
            # Variant can be any string, no validation needed
        
        # Additional validation: if there are more than 3 parts, they are all part of variant
        # Already handled by joining.
        
        return Locale(language, country, variant)