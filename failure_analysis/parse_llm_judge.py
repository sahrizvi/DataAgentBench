import os
import re

def parse_responses(fm_list, responses):
    """
    Parse the LLM responses to extract yes/no answers for each failure mode.
    
    Args:
        responses: List of LLM responses evaluating traces
        
    Returns:
        Dictionary mapping failure mode codes to lists of binary values (0 for no, 1 for yes)
    """

    m_fm_names = dict()
    m_fm_defns = dict()
    m_fm_examples = dict()
    for fm in fm_list:
        fm_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "taxonomy", fm)
        assert os.path.exists(fm_folder), f"Failure mode folder {fm_folder} does not exist."
        name_file = os.path.join(fm_folder, "name.txt")
        with open(name_file, "r") as f:
            m_fm_names[fm] = f.read().strip()
        definition_file = os.path.join(fm_folder, "definition.txt")
        with open(definition_file, "r") as f:
            m_fm_defns[fm] = f.read().strip()
        example_file = os.path.join(fm_folder, "examples.txt")
        with open(example_file, "r") as f:
            m_fm_examples[fm] = f.read().strip()
    
    # Initialize dictionary with empty lists for each failure mode
    failure_modes = {
        f"FM{i + 1}": [] for i in range(len(fm_list))
    }
    
    for i, response in enumerate(responses):
        try:
            # Clean up the response - remove @@ markers if present
            cleaned_response = response.strip()
            if cleaned_response.startswith('@@'):
                cleaned_response = cleaned_response[2:]
            if cleaned_response.endswith('@@'):
                cleaned_response = cleaned_response[:-2]
            
            # Process each failure mode
            for mode in failure_modes.keys():
                # Various patterns to match different response formats
                patterns = [
                    # Format with C. prefix and colon
                    rf"B\..*?{mode}.*?(yes|no)",
                    # Format with just C prefix without dot
                    rf"B{mode}\s+(yes|no)",
                    # Format with mode directly (with or without spaces)
                    rf"{mode}\s*[:]\s*(yes|no)",
                    rf"{mode}\s+(yes|no)",
                    # Format with newlines
                    rf"{mode}\s*\n\s*(yes|no)",
                    # Format with C prefix and newlines
                    rf"B\.{mode}\s*\n\s*(yes|no)"
                ]
                
                found = False
                for pattern in patterns:
                    matches = re.findall(pattern, cleaned_response, re.IGNORECASE | re.DOTALL)
                    if matches:
                        # Use the first match
                        value = 1 if matches[0].lower() == 'yes' else 0
                        failure_modes[mode].append(value)
                        found = True
                        break
                
                if not found:
                    # If we still can't find a match, try a more general approach
                    # Look for the mode number followed by any text and then yes/no
                    general_pattern = rf"(?:B\.)?{mode}.*?(yes|no)"
                    match = re.search(general_pattern, cleaned_response, re.IGNORECASE | re.DOTALL)
                    
                    if match:
                        value = 1 if match.group(1).lower() == 'yes' else 0
                        failure_modes[mode].append(value)
                    else:
                        # If all attempts fail, default to 'no'
                        print(f"Warning: Could not find mode {mode} in response {i}")
                        failure_modes[mode].append(0)
                    
        except Exception as e:
            print(f"Error processing response {i}: {e}")
            # If there's an error, default to 'no' for all modes for this response
            for mode in failure_modes:
                if len(failure_modes[mode]) <= i:  # Only append if we haven't already
                    failure_modes[mode].append(0)
    
    # Ensure all lists have the same length
    max_length = max(len(values) for values in failure_modes.values())
    for mode in failure_modes:
        if len(failure_modes[mode]) < max_length:
            failure_modes[mode].extend([0] * (max_length - len(failure_modes[mode])))
    
    return failure_modes