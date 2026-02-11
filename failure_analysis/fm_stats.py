import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import json
from pathlib import Path
from datetime import datetime
import time
import logging
import logging_config
from openai import AzureOpenAI, OpenAI
from dotenv import load_dotenv
from failure_analysis.get_prompt import get_prompt
from failure_analysis.get_trace import get_trace
from failure_analysis.parse_llm_judge import parse_responses
import logging_config


model_list = [
    "gemini-2.5-flash",
    "gemini-3-pro",
    "gpt-5-mini",
    "gpt-5.2",
    "gpt5.1",
    "kimi-k2-thinking",
]

task_list = [
    "bookreview",
    "crmarenapro",
    "DEPS_DEV_V1",
    "GITHUB_REPOS",
    "googlelocal",
    "PANCANCER_ATLAS",
    "PATENTS",
    "stockindex",
    "stockmarket",
    "yelp",
    "agnews",
    "music_brainz_20k",
    # "civic_unstructured",
    "paper_unstructured"
]


def collect_responses_per_model_per_task(model, task):
    fm_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"results-{model}", f"query_{task}")
    assert os.path.exists(fm_folder), f"Folder {fm_folder} does not exist."
    response_list = []
    for query_file in os.listdir(fm_folder):
        query_path = os.path.join(fm_folder, query_file)
        with open(query_path, "r", encoding="utf-8") as f:
            for l in f:
                response_json = json.loads(l)
                if response_json['judge_result'] != None:
                    response_list.append(response_json['judge_result']['judge'])

    return response_list

def collect_responses_per_model(model):
    response_list = []
    for task in task_list:
        task_responses = collect_responses_per_model_per_task(model, task)
        response_list.extend(task_responses)
    return response_list


def fm_stats(response_list):
    failure_modes, valid_response_cnt = parse_responses(response_list)
    assert valid_response_cnt <= len(response_list)

    fm_count_list = []
    fm_precentage_list = []
    for i in range(4):
        fm = f"FM{i+1}"
        count = sum(failure_modes[fm])
        fm_count_list.append(count)
        precentage = (count / valid_response_cnt) * 100 if valid_response_cnt > 0 else 0
        fm_precentage_list.append(precentage)
    assert sum(fm_count_list) >= valid_response_cnt
    # assert sum(fm_count_list) <= len(response_list), "Total failure mode count cannot exceed total responses."
    return fm_count_list, fm_precentage_list, valid_response_cnt

if __name__ == "__main__":
    for model in model_list:
        responses = collect_responses_per_model(model)
        fm_count_list, fm_precentage_list, tot_cnt = fm_stats(responses)
        # model,tot_cnt,fm1_cnt,fm2_cnt,fm3_cnt,fm4_cnt,fm1_pct,fm2_pct,fm3_pct,fm4_pct
        print(f"{model},{tot_cnt},{fm_count_list[0]},{fm_count_list[1]},{fm_count_list[2]},{fm_count_list[3]},{fm_precentage_list[0]:.2f},{fm_precentage_list[1]:.2f},{fm_precentage_list[2]:.2f},{fm_precentage_list[3]:.2f}")