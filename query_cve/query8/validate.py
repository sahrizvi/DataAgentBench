def validate(llm_output: str):
    import re
    from pathlib import Path
    gt = round(float(Path(__file__).parent.joinpath("ground_truth.csv").read_text().strip()), 2)
    matches = re.findall(r"(\d+\.\d+)", llm_output)
    for m in matches:
        try:
            if round(float(m), 2) == gt:
                return True, f"matched {gt}"
        except ValueError:
            continue
    return False, f"expected {gt}"
