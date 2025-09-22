import re

def validate(llm_output: str) -> (bool, str):
    """
    Validate if LLM output contains the expected month name.
    Expected: November
    Returns:
        (True, "OK") if found
        (False, reason) if not
    """
    expected = "November"
    months = ["January", "February", "March", "April", "May", "June",
              "July", "August", "September", "October", "November", "December"]

    # Clean the output and check for exact match
    llm_output_clean = llm_output.strip()

    # Check for exact month match (case insensitive)
    if expected.lower() in llm_output_clean.lower():
        print(f"✅ Found expected month: {expected}")
        return True, "OK"

    # Check if any month is mentioned
    found_months = []
    for month in months:
        if month.lower() in llm_output_clean.lower():
            found_months.append(month)

    if found_months:
        reason = f"Found months {found_months}, but expected '{expected}'"
        print(f"❌ {reason}")
        return False, reason
    else:
        reason = "No month name found in LLM output"
        print(f"❌ {reason}")
        return False, reason