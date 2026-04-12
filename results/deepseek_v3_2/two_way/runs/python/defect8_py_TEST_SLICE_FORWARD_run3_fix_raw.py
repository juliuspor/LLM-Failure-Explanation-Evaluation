    @classmethod
    def to_locale(cls, locale_str: str) -> Optional[Locale]:
        if locale_str is None:
            return None
        
        # Split by underscore, but handle consecutive underscores as empty parts
        parts = locale_str.split('_')
        # Reconstruct parts to handle empty strings correctly
        # For example, 'fr__POSIX' -> ['fr', '', 'POSIX']
        # However, split('_') on 'fr__POSIX' gives ['fr', '', 'POSIX']
        # But for 'en_GB' -> ['en', 'GB']
        # For 'en_GB_xxx' -> ['en', 'GB', 'xxx']
        # For 'en' -> ['en']
        
        # Validate that we have between 1 and 3 parts after split
        if len(parts) < 1 or len(parts) > 3:
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        language = parts[0]
        country = ""
        variant = ""
        
        if len(parts) >= 2:
            # The second part could be country or variant if empty country
            if parts[1] == "":
                # This means we have two underscores in a row: language__variant
                # So parts[1] is empty, parts[2] is variant
                if len(parts) == 3:
                    variant = parts[2]
                else:
                    # Actually, if we have only two parts and the second is empty,
                    # that would be like 'fr__' which is invalid because variant missing.
                    # But we'll let validation handle.
                    pass
            else:
                # Second part is non-empty: could be country or variant if only two parts?
                # According to Java locale format, if there are two parts, the second is country.
                # If there are three parts, second is country, third is variant.
                # However, we also need to handle the case where country is empty and variant present.
                # That is represented as two underscores: language__variant.
                # So if len(parts) == 2:
                #   If parts[1] is all uppercase? Actually country codes are uppercase, variant can be anything.
                #   But we cannot rely on casing because variant could be uppercase.
                # Better to follow the original logic: after split, we need to interpret based on length and content.
                # Let's adopt a more robust approach: reconstruct the original string and parse manually.
                pass
        
        # Actually, the original code's logic is flawed for empty country. Let's reimplement from scratch.
        # We'll parse the string manually, similar to the original but handling double underscore.
        # We can iterate through the string and find the positions of underscores.
        # But a simpler approach: use regex? Not allowed maybe.
        # Let's do manual parsing:
        # 1. Check length minimum 2.
        # 2. First two chars must be lowercase letters.
        # 3. Then we look for underscores.
        # We need to handle three formats:
        #   language
        #   language_country
        #   language_country_variant
        #   language__variant  (country empty)
        # So we need to detect if after language we have '__' (two underscores) meaning empty country.
        # We can find the first underscore after language.
        # If the next character after that underscore is also underscore, then country is empty.
        
        # Let's implement:
        length = len(locale_str)
        if length < 2:
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        ch0 = locale_str[0]
        ch1 = locale_str[1]
        if ch0 < 'a' or ch0 > 'z' or ch1 < 'a' or ch1 > 'z':
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        # Find first underscore
        try:
            first_underscore = locale_str.index('_')
        except ValueError:
            first_underscore = -1
        
        if first_underscore == -1:
            # No underscore: just language
            if length == 2:
                return Locale(locale_str, "")
            else:
                # language longer than 2 chars? Actually language can be 2 or 3 letters.
                # ISO 639 alpha-2 or alpha-3. So we should allow length 2 or 3.
                # But the original code only allowed length 2 for language-only? Wait: line 216: if length == 2.
                # That means it only accepts exactly 2 chars for language-only.
                # However, ISO 639 alpha-3 codes exist. The original Java Locale can handle 3-letter language codes.
                # The bug report is about empty country, not about 3-letter language.
                # We'll stick to the original validation for now, but note that the original code also had the same limitation.
                # Actually, the original code's condition: if length != 2 and length != 5 and length < 7.
                # That means language-only must be exactly 2 chars. So we keep that.
                if length == 2:
                    return Locale(locale_str, "")
                else:
                    raise ValueError(f"Invalid locale format: {locale_str}")
        
        # We have at least one underscore
        if first_underscore != 2 and first_underscore != 3:
            # Language must be 2 or 3 chars? Actually Java Locale allows 2 or 3 letter language.
            # But the original code assumed language is exactly 2 chars (since it checks indices 0 and 1).
            # We'll keep the original assumption: language is exactly 2 chars.
            # So first_underscore must be 2.
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        language = locale_str[0:first_underscore]
        
        # Check if there is a second underscore immediately after the first
        if first_underscore + 1 < length and locale_str[first_underscore + 1] == '_':
            # Empty country: format language__variant
            country = ""
            # The variant starts after the double underscore
            variant_start = first_underscore + 2
            if variant_start >= length:
                # No variant after double underscore? That's invalid.
                raise ValueError(f"Invalid locale format: {locale_str}")
            variant = locale_str[variant_start:]
            # Validate variant? Not needed.
            return Locale(language, country, variant)
        else:
            # Not empty country: could be language_country or language_country_variant
            # We need to check if there is another underscore later.
            # The country is exactly 2 uppercase letters? Actually country can be 2 or 3 letters (UN M.49).
            # But original code assumed 2 uppercase letters.
            # We'll follow original: country is exactly 2 uppercase letters.
            if first_underscore + 2 >= length:
                raise ValueError(f"Invalid locale format: {locale_str}")
            ch3 = locale_str[first_underscore + 1]
            ch4 = locale_str[first_underscore + 2]
            if ch3 < 'A' or ch3 > 'Z' or ch4 < 'A' or ch4 > 'Z':
                raise ValueError(f"Invalid locale format: {locale_str}")
            country = locale_str[first_underscore + 1: first_underscore + 3]
            
            # Check for variant
            if first_underscore + 3 < length:
                # There is more after country
                if locale_str[first_underscore + 3] != '_':
                    raise ValueError(f"Invalid locale format: {locale_str}")
                variant_start = first_underscore + 4
                if variant_start >= length:
                    raise ValueError(f"Invalid locale format: {locale_str}")
                variant = locale_str[variant_start:]
                return Locale(language, country, variant)
            else:
                # No variant
                return Locale(language, country, "")
