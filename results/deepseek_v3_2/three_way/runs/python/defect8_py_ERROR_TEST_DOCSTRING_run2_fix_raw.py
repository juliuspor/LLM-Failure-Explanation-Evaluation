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
        
        # If length is 2, only language
        if length == 2:
            return Locale(locale_str, "")
        
        # Must have at least one underscore after language
        if locale_str[2] != '_':
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        # If length is 3, only language and underscore (invalid? but we'll treat as language only?)
        # Actually, length 3 would be like "en_", which is invalid per Java's Locale.
        # We'll handle it by checking if after underscore there is any content.
        if length == 3:
            # Only language and underscore, no country or variant. This is invalid.
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        # Now we have at least 4 characters: "en_A" or "en__"
        # Check if the character after underscore is another underscore (empty country)
        if locale_str[3] == '_':
            # Empty country, variant starts after second underscore
            # language = locale_str[0:2]
            # country = ""
            # variant = locale_str[4:]  # after the double underscore
            # But need to ensure there is at least something after the double underscore?
            # In Java, variant can be empty? Probably not, but we'll allow empty variant.
            # However, the format "fr__" would be language="fr", country="", variant=""
            # That's equivalent to just "fr", but with extra underscores.
            # We'll treat it as language only? Actually, Java's Locale.forLanguageTag handles "fr__"?
            # Let's stick to the underscore format: language + "_" + country + "_" + variant
            # If country is empty, then we have language + "__" + variant.
            # So variant starts at index 4.
            # If length is 4, then variant is empty string.
            return Locale(locale_str[0:2], "", locale_str[4:])
        else:
            # Country is present, must be two uppercase letters
            if length < 5:
                raise ValueError(f"Invalid locale format: {locale_str}")
            ch3 = locale_str[3]
            ch4 = locale_str[4]
            if ch3 < 'A' or ch3 > 'Z' or ch4 < 'A' or ch4 > 'Z':
                raise ValueError(f"Invalid locale format: {locale_str}")
            
            # Now we have language and country.
            if length == 5:
                return Locale(locale_str[0:2], locale_str[3:5])
            else:
                # Must have another underscore before variant
                if locale_str[5] != '_':
                    raise ValueError(f"Invalid locale format: {locale_str}")
                # variant is everything after the second underscore
                return Locale(locale_str[0:2], locale_str[3:5], locale_str[6:])