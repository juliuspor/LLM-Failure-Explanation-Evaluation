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
        
        # Handle special cases like 'C', 'POSIX', 'en_US.UTF-8'
        # First, split by '.' to remove encoding
        parts = locale_str.split('.')
        locale_part = parts[0]
        
        # Handle special locale names
        if locale_part in ('C', 'POSIX'):
            # These are special locales that don't follow language/country pattern
            # Return a Locale with empty language and country, variant set to the special name
            return Locale("", "", locale_part)
        
        # Now parse the language_country_variant part
        # Split by underscore
        subparts = locale_part.split('_')
        
        # Validate number of parts
        if len(subparts) == 0 or len(subparts) > 3:
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        language = subparts[0]
        if not language:
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        # Validate language code (2 or 3 letters, all lowercase)
        if not (2 <= len(language) <= 3 and language.isalpha() and language.islower()):
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        country = ""
        variant = ""
        
        if len(subparts) >= 2:
            country = subparts[1]
            # Country code can be 2 letters (ISO 3166) or 3 digits (UN M.49)
            if country:
                if not (len(country) == 2 and country.isalpha() and country.isupper() or
                        len(country) == 3 and country.isdigit()):
                    raise ValueError(f"Invalid locale format: {locale_str}")
            else:
                # Empty country part (like 'fr__POSIX' after split) becomes variant
                # Actually, if country part is empty, we should treat the next part as variant
                # But we already split by '_', so empty strings appear in list
                # We need to handle this differently.
                # Let's reconstruct: if we have ['fr', '', 'POSIX'], then language='fr', country='', variant='POSIX'
                # But our current logic would set country='' and then variant from subparts[2]
                pass
        
        if len(subparts) >= 3:
            variant = subparts[2]
            # Variant can be any string, but we should handle empty strings
            if not variant:
                variant = ""
        
        # If there are more than 3 subparts (due to multiple underscores), join the rest as variant
        if len(subparts) > 3:
            variant = '_'.join(subparts[2:])
        
        return Locale(language, country, variant)