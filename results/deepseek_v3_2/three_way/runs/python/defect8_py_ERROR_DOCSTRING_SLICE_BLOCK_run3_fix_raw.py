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
        # Remove empty strings that result from consecutive underscores? Actually, we need to preserve them as empty segments.
        # But the Java Locale parsing treats consecutive underscores as empty country or variant.
        # For example, "fr__POSIX" -> language="fr", country="", variant="POSIX"
        # So we need to handle the case where we have more than 3 parts due to empty segments.
        # Let's re-parse more robustly.
        
        # We'll iterate through the string and find the positions of underscores.
        # But simpler: we can use the original logic but adjust for empty segments.
        # The Java implementation in LocaleUtils (from Apache Commons) handles this.
        # Looking at the original Java code, it does:
        #   int len = str.length();
        #   if (len != 2 && len != 5 && len < 7) {
        #       throw new IllegalArgumentException("Invalid locale format: " + str);
        #   }
        #   ...
        # That's exactly what we have, but it fails for "fr__POSIX" because length is 9, but the check expects at least 7.
        # Actually length 9 passes the length check (>=7). Then it checks:
        #   if (str.charAt(2) != '_') ...
        #   ch3 = str.charAt(3); ch4 = str.charAt(4);
        #   if (ch3 < 'A' || ch3 > 'Z' || ch4 < 'A' || ch4 > 'Z') ...
        # For "fr__POSIX", str.charAt(2) is '_' (ok), but ch3 is '_' (not uppercase letter) -> error.
        # So we need to handle empty country code.
        # The Java Locale class itself can parse "fr__POSIX" via the constructor Locale(String language, String country, String variant).
        # But LocaleUtils.toLocale is stricter.
        # However, the bug report says the function fails for "fr__POSIX". We need to fix it to accept such format.
        # Let's implement a more flexible parsing: split by '_' and then interpret.
        # According to Java Locale, the format is: language + "_" + country + "_" + variant
        # where country and variant can be empty. So "fr__POSIX" means language=fr, country=empty, variant=POSIX.
        # Similarly, "en__POSIX" etc.
        # So we can parse by splitting on '_' and then assign parts.
        # But note: variant can contain underscores? In Java, variant is the rest after the second underscore.
        # So we need to split into at most 3 parts, but keep empty strings for missing parts.
        # We can use partition twice.
        
        # First, find the first underscore.
        first_underscore = locale_str.find('_')
        if first_underscore == -1:
            # No underscore: just language
            language = locale_str
            country = ''
            variant = ''
        else:
            language = locale_str[:first_underscore]
            rest = locale_str[first_underscore+1:]
            # Now find the second underscore in the rest
            second_underscore = rest.find('_')
            if second_underscore == -1:
                # Only one underscore: language_country, rest is country
                country = rest
                variant = ''
            else:
                # Two or more underscores: country is before second underscore, variant is after
                country = rest[:second_underscore]
                variant = rest[second_underscore+1:]
        
        # Validate language: must be two letters, lowercase? Actually ISO 639 can be 2 or 3 letters.
        # But the original code only accepted 2-letter language codes? It checked first two characters are lowercase.
        # We'll keep the validation similar but more flexible.
        if not language:
            raise ValueError(f"Invalid locale format: {locale_str}")
        for ch in language:
            if ch < 'a' or ch > 'z':
                raise ValueError(f"Invalid locale format: {locale_str}")
        
        # Validate country: if present, must be two uppercase letters or empty
        if country:
            if len(country) != 2:
                # Could be three-digit UN M.49? The Locale constructor allows any string for country.
                # But the original validation expected exactly two uppercase letters.
                # We'll relax to allow any uppercase letters? Actually Java Locale allows any two uppercase letters or three digits.
                # We'll follow the original stricter validation for compatibility.
                # However, for "fr__POSIX", country is empty, so we skip.
                # For other cases, we want to accept two uppercase letters.
                # Let's check: if country length is 2, both uppercase; else raise.
                raise ValueError(f"Invalid locale format: {locale_str}")
            for ch in country:
                if ch < 'A' or ch > 'Z':
                    raise ValueError(f"Invalid locale format: {locale_str}")
        
        # Variant can be any string, no validation needed.
        
        return Locale(language, country, variant)