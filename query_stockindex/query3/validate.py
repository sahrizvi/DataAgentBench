def validate(llm_output: str):
    """All name+country pairs appear with country (or alias) within 100 chars
    of the ticker (in either direction). Order not enforced."""
    gt_pairs = [
        ("399001.SZ", "China"),
        ("NSEI", "India"),
        ("IXIC", "United States"),
        ("000001.SS", "China"),
        ("NYA", "United States"),
    ]
    country_aliases = {
        "china": ["china", "cn"],
        "india": ["india", "in"],
        "united states": ["united states", "us", "usa", "u.s."],
    }

    llm_lower = llm_output.lower()
    for name, country in gt_pairs:
        name_lower = name.lower()
        idx = llm_lower.find(name_lower)
        if idx == -1:
            return False, f"Missing name: {name}"
        aliases = country_aliases.get(country.lower(), [country.lower()])
        lo = max(0, idx - 100)
        hi = min(len(llm_lower), idx + len(name_lower) + 100)
        window = llm_lower[lo:hi]
        if not any(a in window for a in aliases):
            return False, f"Country '{country}' not within ±100 chars of '{name}'"
    return True, "All name-country pairs matched."
