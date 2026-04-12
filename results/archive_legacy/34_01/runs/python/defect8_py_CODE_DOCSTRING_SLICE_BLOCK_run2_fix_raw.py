@classmethod
    def to_locale(cls, locale_str: str) -> Optional[Locale]:
        if locale_str is None:
            return None
        import re
        pattern = re.compile(r'^[a-z]{2}(?:_[A-Z]{2}(?:_.+)?|_.+)?$')
        if not pattern.match(locale_str):
            raise ValueError(f"Invalid locale format: {locale_str}")
        parts = locale_str.split('_', 2)
        if len(parts) == 1:
            return Locale(parts[0], "")
        if len(parts) == 2:
            if len(parts[1]) == 0:
                raise ValueError(f"Invalid locale format: {locale_str}")
            if len(parts[1]) == 2 and parts[1].isupper():
                return Locale(parts[0], parts[1])
            else:
                return Locale(parts[0], "", parts[1])
        return Locale(parts[0], parts[1], parts[2])