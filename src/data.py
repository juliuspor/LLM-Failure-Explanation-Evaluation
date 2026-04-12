# Defects with Python translations of Defects4J files
# defect1_py start_line: 396
# defect2_py start_line: 71
# defect3_py start_line: 154
# defect4_py start_line: 377
# defect5_py start_line: 347
# defect7_py start_line: 766
# defect8_py start_line: 239
# defect6_py start_line: 176
# defect9_py start_line: 28
# defect10_py start_line: 37
# defect11_py start_line: 35
# defect12_py start_line: 56

python_defects = [
    {
        "id": "defect1_py",
        "source_path": "failures/python_defects/hit01_timezone.py",
        "test_path": "failures/python_defects/tests/test_hit01_complete.py",
        "function_name": "DateTimeZone.for_offset_hours_minutes",
        "error": "Test failed with ValueError: Minutes out of range: -15",
        "ground_truth": "The `for_offset_hours_minutes` function throws a `ValueError` because it strictly validates that minutes must be in the range [0, 59], rejecting negative minutes (e.g., -15). This prevents creating time zones with negative offsets like `-02:15` using the intuitive arguments `(-2, -15)`, which the test expects to work."
    },
    {
        "id": "defect2_py",
        "source_path": "failures/python_defects/hit02_grayscale.py",
        "test_path": "failures/python_defects/tests/test_hit02_complete.py",
        "function_name": "GrayPaintScale.get_paint",
        "error": "Test failed with ValueError: Color parameter outside of expected range: Red Green Blue",
        "ground_truth": "The `get_paint` method correctly calculates the clamped value `v` but incorrectly uses the original, unclamped `value` to calculate the grayscale intensity `g`. When `value` is negative (e.g., -0.5), `g` becomes negative (e.g., -127), causing a `ValueError` because RGB values must be in range 0-255."
    },
    {
        "id": "defect3_py",
        "source_path": "failures/python_defects/hit03_translator.py",
        "test_path": "failures/python_defects/tests/test_hit03_complete.py",
        "function_name": "CharSequenceTranslator.translate",
        "error": "Test failed with IndexError: String index out of range: 2",
        "ground_truth": "The `translate` method throws an `IndexError` when processing surrogate pairs (like emoji characters). The `CsvEscaper.translate_codepoint` incorrectly returns 2 for a surrogate pair (indicating 2 codepoints consumed), but a surrogate pair represents only 1 codepoint encoded as 2 code units. The translation loop then tries to advance `pos` twice, accessing an out-of-bounds index on the second iteration."
    },
    {
        "id": "defect4_py",
        "source_path": "failures/python_defects/hit04_timeperiod.py",
        "test_path": "failures/python_defects/tests/test_hit04_complete.py",
        "function_name": "TimePeriodValues._update_bounds",
        "error": "Test failed with AssertionError: Expected max_middle_index=1, got 3",
        "ground_truth": "The `_update_bounds` method incorrectly uses `_min_middle_index` instead of `_max_middle_index` when looking up the current maximum middle period for comparison. When adding a new item, it compares the new item's middle value against the minimum middle period's value instead of the maximum. This causes incorrect updates to `_max_middle_index` when items with middle values between the min and max are added."
    },
    {
        "id": "defect5_py",
        "source_path": "failures/python_defects/hit05_arrayutils.py",
        "test_path": "failures/python_defects/tests/test_hit05_complete.py",
        "function_name": "ArrayUtils.add",
        "error": "Test failed with TypeError: Cannot cast object list to str list (ClassCastException: [Ljava.lang.Object; cannot be cast to [Ljava.lang.str;)",
        "ground_truth": "The `add` method fails in the `(array=None, element=None, expected_type=str)` case: it infers `inferred_type = object` (because both inputs are None) and ignores `expected_type` during inference, then raises a `TypeError` in the type-check step (`inferred_type == object and expected_type != object`), simulating Java’s `Object[]` → `String[]` `ClassCastException`. The method should use `expected_type` as the inferred component type (or skip the cast error) in this specific case and simply return `[None]` without raising a TypeError."
    },
    {
        "id": "defect6_py",
        "source_path": "failures/python_defects/hit06_codeconsumer.py",
        "test_path": "failures/python_defects/tests/test_hit06_complete.py",
        "function_name": "CodeConsumer.add_number",
        "error": "Test failed with AssertionError: Expected -0.0, got 0",
        "ground_truth": "The `add_number` method checks `if x < 0 and prev == '-':` to add space, but fails to handle negative zero specifically for printing. When checking `if x == int(x)`, negative zero satisfies this (0.0 == 0), entering the integer block which prints '0' instead of preserving the formatting as '-0.0' or '-0'."
    },
    {
        "id": "defect7_py",
        "source_path": "failures/python_defects/hit07_classutils.py",
        "test_path": "failures/python_defects/tests/test_hit07_complete.py",
        "function_name": "ClassUtils.to_class",
        "error": "Test failed with AttributeError: 'NoneType' object has no attribute 'upper'",
        "ground_truth": "The `to_class` function throws an `AttributeError` when the input list contains a `None` element. The function iterates over the array calling a method on each element without checking for None. The function should handle `None` inputs by mapping them to `type(None)` in the returned list."
    },
    {
        "id": "defect8_py",
        "source_path": "failures/python_defects/hit08_locale.py",
        "test_path": "failures/python_defects/tests/test_hit08_complete.py",
        "function_name": "LocaleUtils.to_locale",
        "error": "Test failed with ValueError: Invalid locale format: fr__POSIX",
        "ground_truth": "The `to_locale` function fails to parse the locale string `fr__POSIX` because it strictly expects characters at positions 3-4 to be uppercase letters (a country code). For the input `fr__POSIX`, the character at position 3 is `_`, which fails this check. The function lacks logic to handle the `language__variant` format where the country code is empty (indicated by the double underscore)."
    },
    {
        "id": "defect9_py",
        "source_path": "failures/python_defects/hit09_stringutils.py",
        "test_path": "failures/python_defects/tests/test_hit09_complete.py",
        "function_name": "StringUtils.replace_each",
        "error": "Test failed with TypeError: object of type 'NoneType' has no len()",
        "ground_truth": "The `replace_each` method should ignore replacement pairs where `search_list[i]` or `replacement_list[i]` is `None` (mirroring Java's intent to skip null elements). The buggy implementation correctly skips `None` entries when searching for matches, but then later computes buffer growth using `len(replacement_list[i]) - len(search_list[i])` without guarding `None`, causing a crash (analogous to a Java `NullPointerException`)."
    },
    {
        "id": "defect10_py",
        "source_path": "failures/python_defects/hit10_numberutils.py",
        "test_path": "failures/python_defects/tests/test_hit10_complete.py",
        "function_name": "NumberUtils.create_number",
        "error": "Test failed with IndexError: String index out of range: 0",
        "ground_truth": "The `create_number` method handles type qualifiers like 'l'/'L' by stripping the last character and then checking the first character of the remaining numeric string. For inputs like \"l\" or \"L\", stripping the qualifier produces an empty string, and the buggy code performs a Java-like `charAt(0)` on it, raising an out-of-range error instead of a clean `ValueError` (Java `NumberFormatException`)."
    },
    {
        "id": "defect11_py",
        "source_path": "failures/python_defects/hit11_randomstringutils.py",
        "test_path": "failures/python_defects/tests/test_hit11_complete.py",
        "function_name": "RandomStringUtils.random",
        "error": "Test failed with AssertionError: Message (bound must be positive) must contain 'start'",
        "ground_truth": "The `random` method fails to validate explicit `start`/`end` bounds when `end <= start`. For `random(3, 5, 5, false, false)`, it computes a zero-width range and then triggers a lower-level `ValueError` with message \"bound must be positive\" (mirroring Java's `Random#nextInt`). The correct behavior is to detect `end <= start` up front and raise an error message that mentions both `start` and `end` (e.g., \"Parameter end (...) must be greater than start (...)\")."
    },
    {
        "id": "defect12_py",
        "source_path": "failures/python_defects/hit12_wordutils.py",
        "test_path": "failures/python_defects/tests/test_hit12_complete.py",
        "function_name": "WordUtils.abbreviate",
        "error": "Test failed with IndexError: String index out of range: 15",
        "ground_truth": "The `abbreviate` method clamps `upper` to `len(text)` but then forces `upper = lower` when `upper < lower`. If `lower` is greater than the string length (e.g., lower=15 for a 10-char string), this makes `upper` out of bounds. The buggy code then calls a Java-like substring with `end=upper`, which raises an out-of-range error instead of returning the original string."
    }
]
