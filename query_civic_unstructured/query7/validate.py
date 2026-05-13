GROUND_TRUTH = [
    "Clover Heights Storm Drain",
    "Encinal Canyon Road Drainage Improvements",
    "Encinal Canyon Road Drainage Improvements (FEMA/CalOES Project)",
    "Latigo Canyon Road Culvert Repairs",
    "Latigo Canyon Road Culvert Repairs (FEMA/CalOES Project)",
    "Outdoor Warning Sirens (FEMA)",
    "Storm Drain Master Plan",
]


def validate(llm_output: str):
    text = llm_output.lower()
    missing = [p for p in GROUND_TRUTH if p.lower() not in text]
    if not missing:
        return True, "All ground truth project names found in LLM output."
    reason = f"Missing project(s) in LLM output: {missing}"
    return False, reason
