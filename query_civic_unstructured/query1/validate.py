GROUND_TRUTH = [
    "2022 Annual Street Maintenance",
    "Annual Street Maintenance",
    "Civic Center Water Treatment Facility Phase 2",
    "Marie Canyon Green Streets",
    "Michael Landon Center Roof Replacement Project",
    "PCH Median Improvements Project",
    "PCH Signal Synchronization System Improvements Project",
    "PCH at Trancas Canyon Road Right Turn Lane",
    "Permanent Skate Park",
    "Westward Beach Road Improvements Project",
    "Westward Beach Road Repair Project",
]


def validate(llm_output: str):
    text = llm_output.lower()
    missing = [p for p in GROUND_TRUTH if p.lower() not in text]
    if not missing:
        return True, "All ground truth project names found in LLM output."
    reason = f"Missing project(s) in LLM output: {missing}"
    return False, reason
