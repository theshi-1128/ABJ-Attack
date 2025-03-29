from utils.json2data import format_json_to_data
from pipeline.pipeline_prompt import query_transform


def get_data(task, model):
    json_data = model.generate_response(query_transform.format(HB=task))
    data = format_json_to_data(json_data)
    return data