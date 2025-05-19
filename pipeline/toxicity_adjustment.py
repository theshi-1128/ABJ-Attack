from utils.clean_text import clean_text
from utils.json2data import format_json_to_data
from utils.print_helper import print_judgment
from pipeline.pipeline_prompt import toxicity_enhancement, toxicity_reduction, detailed_judge_prompt


def toxicity_adjustment(response, data, judge_model, assist_model):
    new_json_data = data
    judgment = clean_text(judge_model.generate_response(detailed_judge_prompt.format(PROMPT=response)))
    print_judgment(judgment)
    # toxicity enhancement
    if '1' not in judgment:
        new_json_data = assist_model.generate_response(toxicity_enhancement.format(DATA=data))
    # toxicity reduction
    elif '1' in judgment:
        new_json_data = assist_model.generate_response(toxicity_reduction.format(DATA=data))
    new_data = format_json_to_data(new_json_data)
    return new_data

