import re

def validate(llm_output: str) -> (bool, str):
    """
    Validate LLM output:
    - Ground truth is 0.3333333333333333
    - Accept if any float in LLM output rounds to 0.33
    """
    ground_truth = 0.3333333333333333
    gt_rounded = round(ground_truth, 2)  # → 0.33

    # Extract all float-like numbers from LLM output
    matches = re.findall(r"\d+\.\d+", llm_output)
    for m in matches:
        try:
            val = float(m)
            if round(val, 2) == gt_rounded:
                print(f"✅ Found matching value: {val} → ~{gt_rounded}")
                return True, "OK"
        except:
            continue

    reason = f"❌ No value in LLM output rounds to {gt_rounded}"
    print(reason)
    return False, reason
