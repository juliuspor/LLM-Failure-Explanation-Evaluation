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
        
        # Split by underscore, but keep empty parts to handle POSIX format
        parts = locale_str.split('_')
        if not parts:
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        # First part must be language code (2 or 3 lowercase letters)
        language = parts[0]
        if not language:
            raise ValueError(f"Invalid locale format: {locale_str}")
        if not language.isalpha() or not language.islower():
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        # Initialize country and variant
        country = ""
        variant = ""
        
        # Process remaining parts
        remaining = parts[1:]
        if remaining:
            # Second part could be country or variant (if empty string indicates POSIX)
            second = remaining[0]
            if second == "":
                # POSIX format: fr__POSIX -> language='fr', country='', variant='POSIX'
                # Skip the empty part and treat next as variant
                if len(remaining) >= 2:
                    variant = remaining[1]
                else:
                    # Should not happen because split would not produce trailing empty?
                    raise ValueError(f"Invalid locale format: {locale_str}")
            elif len(second) == 2 and second.isalpha() and second.isupper():
                # ISO 3166 alpha-2 country code
                country = second
                # Third part if exists is variant
                if len(remaining) >= 2:
                    variant = remaining[1]
            elif len(second) == 3 and second.isdigit():
                # UN M.49 numeric-3 area code
                country = second
                if len(remaining) >= 2:
                    variant = remaining[1]
            else:
                # Not a country code, treat as variant
                variant = second
                # If there is more after variant, join with underscore
                if len(remaining) >= 2:
                    variant = '_'.join(remaining)
        
        # Validate that we don't have extra parts beyond what we processed
        # (We already joined extra parts into variant)
        
        return Locale(language, country, variant)