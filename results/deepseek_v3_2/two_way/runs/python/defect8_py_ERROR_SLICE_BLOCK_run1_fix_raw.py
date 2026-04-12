    @classmethod
    def to_locale(cls, locale_str: str) -> Optional[Locale]:
        if locale_str is None:
            return None
        
        length = len(locale_str)
        if length < 2:
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        # Validate first two characters are lowercase letters
        ch0 = locale_str[0]
        ch1 = locale_str[1]
        if ch0 < 'a' or ch0 > 'z' or ch1 < 'a' or ch1 > 'z':
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        if length == 2:
            return Locale(locale_str, "")
        
        # Check for separator after language
        if locale_str[2] != '_':
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        if length == 3:
            # Only language and underscore (e.g., "en_")
            return Locale(locale_str[0:2], "")
        
        # Now we have at least 4 characters: "xx_" + something
        # The part after the first underscore could be country, variant, or empty.
        # We need to parse according to the pattern: language + "_" + country + "_" + variant
        # But country may be missing (e.g., "fr__POSIX") or variant may be missing.
        # We'll split by underscore, but we need to handle empty segments.
        # The Java Locale constructor allows empty country and variant.
        # The original code assumed exactly 5 or >=7 characters, which is too restrictive.
        # Let's split the string by '_' and handle each part.
        parts = locale_str.split('_')
        # First part is language (already validated)
        language = parts[0]
        country = ""
        variant = ""
        if len(parts) > 1:
            # Second part could be country or variant if country is empty.
            # According to Java Locale, country must be two uppercase letters or three digits.
            # But we also have cases like "fr__POSIX" where country is empty and variant is "POSIX".
            # In that case, parts[1] is empty string.
            # We need to iterate through parts after language.
            # The first non-empty part after language is country if it's two letters or three digits.
            # But the original validation expected uppercase letters for country.
            # However, the Java Locale also accepts numeric country codes (UN M.49).
            # We'll follow the original implementation's validation: country must be two uppercase letters.
            # But the bug is that we need to allow empty country (i.e., double underscore).
            # So we need to handle the case where the second part is empty.
            # Let's reconstruct: we have language, then an underscore, then possibly country, then possibly variant.
            # The string may have multiple underscores.
            # We'll use the same logic as the original but allow empty country.
            # Actually, the original code expected exactly 5 characters for language_country (e.g., en_US).
            # That's wrong for "fr__POSIX".
            # We'll implement a more robust parsing:
            # 1. language is first two chars (already validated).
            # 2. Find the next segment after the first underscore that is non-empty.
            # 3. If that segment is two uppercase letters, treat as country.
            # 4. If there is another segment after that, treat as variant.
            # But we must also allow numeric country codes? The original code didn't.
            # Let's stick to the original validation for country: two uppercase letters.
            # However, the bug report is about "fr__POSIX". In that case, the country is empty.
            # So we need to allow the country to be empty, and the variant starts after two underscores.
            # We can parse by splitting on '_' and then assign parts.
            # The Java Locale constructor takes (language, country, variant).
            # The string format is: language + "_" + country + "_" + variant
            # But country may be omitted, in which case there is an extra underscore.
            # So we can have: language + "_" + "_" + variant
            # Or language + "_" + country
            # Or language + "_" + country + "_" + variant
            # We'll handle by splitting and then checking the number of parts.
            # However, note that variant can contain underscores? In Java, variant is a single string.
            # The variant is everything after the second underscore.
            # So we can split into at most 3 parts: language, country, variant.
            # But if there are multiple underscores, variant may contain underscores.
            # Actually, Java Locale's toString() returns language + "_" + country + "_" + variant.
            # If variant contains underscores, they are preserved.
            # So we need to split with a limit of 3.
            parts = locale_str.split('_', 2)  # maxsplit=2
            # Now parts[0] is language, parts[1] is country (or empty), parts[2] is variant (if present).
            # But if there is only one underscore, parts will have length 2.
            # If there are two underscores, parts will have length 3.
            # However, note that "fr__POSIX" split with maxsplit=2 gives ['fr', '', 'POSIX'].
            # That's perfect.
            # Now we need to validate country if it is non-empty.
            language = parts[0]
            if len(parts) > 1:
                country = parts[1]
                if len(country) > 0:
                    # Country must be two uppercase letters (or numeric? but original didn't).
                    if len(country) != 2 or country[0] < 'A' or country[0] > 'Z' or country[1] < 'A' or country[1] > 'Z':
                        raise ValueError(f"Invalid locale format: {locale_str}")
            if len(parts) > 2:
                variant = parts[2]
            return Locale(language, country, variant)
        
        # This should not be reached
        raise ValueError(f"Invalid locale format: {locale_str}")