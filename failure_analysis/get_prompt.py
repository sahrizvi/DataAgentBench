import os

def get_prompt(fm_list, trace) -> str:
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

    
    prompt = (
        "Below I will provide the trace of a **failed** task of a data agent. "
        "Provide me an analysis of the failure modes as I will say below.\n"
        "There are several failure modes I identified. I will provide them below. Tell me if you encounter any of them, as a binary yes or no.\n"
        "Also, give me a one sentence (be brief) summary of the problems with the failure modes in the trace. Only mark a failure mode if you can provide an example of it in the trace, and specify that in your summary at the end.\n"
        "At the very end, I provide you with the definitions and examples of the failure modes for you to understand them better.\n"
        "Tell me if you encounter any of these failure modes between the @@ symbols as I will say below, as a binary yes or no.\n"
        "Here are the things you should answer. Start after the @@ sign and end before the next @@ sign (do not include the @@ symbols in your answer):\n"
        "*** begin of things you should answer *** @@\n"
        "A. Freeform text summary of the problems with the failure modes in the trace: <summary>\n"
        "B. Whether you encounter any of the failure modes:\n"
    ) + "\n".join([
        f"FM{i + 1} {m_fm_names[fm_list[i]]}: <yes or no>" for i in range(len(fm_list))
    ]) 
    prompt += "\n" + (
        "@@*** end of your answer ***\n"
        "An example answer is: \n"
        "A. The task is failed because...\n"
        "B. \n")
    prompt += "\n".join([f'FM{i + 1} yes/no' for i in range(len(fm_list))]) + "\n\n"
        
    prompt += ("Here is the trace:\n"
        f"{trace.strip()}"
        "\nTrace End\n\n"
        "Here are the definitions and examples of the failure modes:\n"
    )
    prompt += "\n\n".join([
        f"FM{i + 1} {m_fm_names[fm_list[i]]}:\n"
        f"Definition:\n{m_fm_defns[fm_list[i]]}\n"
        f"Examples:\n{m_fm_examples[fm_list[i]]}\n\n"
        for i in range(len(fm_list))
    ])

    return prompt.strip()