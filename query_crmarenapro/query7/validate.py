import re

def validate(llm_output: str) -> (bool, str):
    """
    Validate if LLM output contains the expected knowledge article ID or None.
    Expected: ka0Wt000000EoD3IAK
    Returns:
        (True, "OK") if found
        (False, reason) if not
    """
    expected = "ka0Wt000000EoD3IAK"

    # Clean the output and check for exact match
    llm_output_clean = llm_output.strip()

    # Check for exact ID match (case sensitive for IDs)
    if expected in llm_output_clean:
        print(f"✅ Found expected knowledge article ID: {expected}")
        return True, "OK"

    # Check if any knowledge article ID pattern is present (starts with 'ka0')
    ka_pattern = r'ka0[A-Za-z0-9]{15}'
    found_ids = re.findall(ka_pattern, llm_output_clean)

    if found_ids:
        reason = f"Found knowledge article IDs {found_ids}, but expected '{expected}'"
        print(f"❌ {reason}")
        return False, reason
    else:
        # Check for "None" response (which would be incorrect for this case)
        if re.search(r'\b(none|no violation|no policy violation)\b', llm_output_clean, re.IGNORECASE):
            reason = "LLM output indicates no policy violation, but expected knowledge article ID"
            print(f"❌ {reason}")
            return False, reason
        else:
            reason = "No knowledge article ID found in LLM output"
            print(f"❌ {reason}")
            return False, reason