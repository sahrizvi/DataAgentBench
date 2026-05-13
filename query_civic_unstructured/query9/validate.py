GROUND_TRUTH = [
    "Emergency Relief Fund",
    "Municipal Fund",
    "Private Donation",
    "Public-Private Partnership",
]


def validate(llm_output: str):
    text = llm_output.lower()
    missing = [s for s in GROUND_TRUTH if s.lower() not in text]
    if not missing:
        return True, "All ground truth funding sources found in LLM output."
    reason = f"Missing funding source(s) in LLM output: {missing}"
    return False, reason
