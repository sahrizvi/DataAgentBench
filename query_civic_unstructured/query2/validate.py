import re

GT_PROJECT = "Guardrail Replacement Citywide (FEMA Project)"
GT_AMOUNT = 12519000


def extract_numeric_values(text):
    values = []
    for num in re.findall(r'\b[\d,]+(?:\.\d+)?\b', text):
        try:
            values.append(float(num.replace(",", "")))
        except ValueError:
            pass
    return values


def validate(llm_output: str):
    text = llm_output.lower()

    name_found = GT_PROJECT.lower() in text
    amount_found = any(abs(v - GT_AMOUNT) == 0 for v in extract_numeric_values(llm_output))

    if name_found and amount_found:
        return True, "Ground truth project name and amount found in LLM output."
    missing = []
    if not name_found:
        missing.append(f"project name '{GT_PROJECT}'")
    if not amount_found:
        missing.append(f"amount '{GT_AMOUNT}'")
    return False, f"Missing in LLM output: {', '.join(missing)}"
