    @classmethod
    def to_locale(cls, locale_str: str) -> Optional[Locale]:
        if locale_str is None:
            return None
        
        parts = locale_str.split('_')
        if not parts:
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        language = parts[0]
        if len(language) != 2 or not language.isalpha() or not language.islower():
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        country = ""
        variant = ""
        
        if len(parts) > 1:
            country_part = parts[1]
            if country_part:
                if len(country_part) != 2 or not country_part.isalpha() or not country_part.isupper():
                    # Could be a variant if it's not a 2-letter uppercase country code
                    # But according to Java Locale, country must be uppercase letters or digits.
                    # However, we need to handle cases like "fr__POSIX" where country is empty.
                    # Actually, if country_part is not a valid country code, we treat it as variant.
                    # But the format "fr__POSIX" has an empty country part between two underscores.
                    # So we need to handle empty strings in parts.
                    # Let's re-evaluate: split('_') on "fr__POSIX" gives ['fr', '', 'POSIX']
                    # So parts[1] is empty string, meaning country is empty.
                    # So we need to check if country_part is empty.
                    pass
            # We'll process by iterating through parts.
        
        # Better approach: iterate through parts after language.
        # According to Java Locale, the format is language + "_" + country + "_" + variant
        # where country is optional but if variant is present, country can be empty (two underscores).
        # So we need to handle empty country.
        
        # Let's implement a more robust parsing:
        # 1. Split by '_' and filter out empty strings? Not exactly, because empty country is allowed.
        # 2. We'll follow the original logic but adjust for empty country.
        # The original code expects exactly 2, 5, or >=7 characters and specific positions.
        # That doesn't handle double underscore.
        # We'll rewrite to handle general case.
        
        # Actually, the Java Locale constructor allows empty country and variant.
        # The string "fr__POSIX" is parsed as language="fr", country="", variant="POSIX".
        # So we need to parse that.
        
        # Let's implement:
        # - language is first part, must be 2 letters lowercase.
        # - If there are more parts:
        #   - second part: if it's length 2 and uppercase, it's country; otherwise it's variant (and country empty).
        #   - But what if second part is empty? That means country empty and third part is variant.
        #   - So we need to consider that parts may have empty strings.
        
        # Simpler: use regex? But we can do with splitting.
        # We'll split with '_' and keep empty strings.
        parts = locale_str.split('_')
        # parts[0] is language
        if len(parts[0]) != 2 or not parts[0].isalpha() or not parts[0].islower():
            raise ValueError(f"Invalid locale format: {locale_str}")
        language = parts[0]
        
        country = ""
        variant = ""
        
        if len(parts) >= 2:
            # Check if parts[1] is a country code (2 uppercase letters)
            if len(parts[1]) == 2 and parts[1].isalpha() and parts[1].isupper():
                country = parts[1]
                # The rest (parts[2:]) joined by '_' is variant
                if len(parts) > 2:
                    variant = '_'.join(parts[2:])
            else:
                # parts[1] is not a country code, so it's part of variant (and country is empty)
                # But also if parts[1] is empty, then country is empty and variant starts from parts[2]
                # Actually, if parts[1] is empty, then we have double underscore.
                # In that case, country is empty and variant is parts[2] (if exists) or empty.
                # So we need to handle empty string in parts[1].
                if parts[1] == '':
                    # country is empty
                    if len(parts) > 2:
                        variant = '_'.join(parts[2:])
                else:
                    # parts[1] is not empty and not a country code -> treat as variant
                    variant = '_'.join(parts[1:])
        
        return Locale(language, country, variant)