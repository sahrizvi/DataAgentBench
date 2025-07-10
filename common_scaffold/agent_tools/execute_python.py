import pandas as pd
from typing import Any

def execute_python(code: str, vars_dict: dict) -> pd.DataFrame | Any:
    """
    Execute LLM-provided Python code in the context of vars_dict.
    The code MUST assign its result to a variable named `result`.

    Args:
        code (str): Python code from LLM.
        vars_dict (dict): The current variable context.

    Returns:
        pd.DataFrame | Any: The value of `result` if present, otherwise the updated vars_dict.
    """
    safe_globals = {"pd": pd}
    local_vars = vars_dict.copy()

    try:
        exec(code, safe_globals, local_vars)
    except Exception as e:
        raise RuntimeError(f"Error executing code: {e}")
    
    vars_dict.update(local_vars)

    if "result" in local_vars:
        vars_dict["result"] = local_vars["result"]
        return local_vars["result"]

    return vars_dict
