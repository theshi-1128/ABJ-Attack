import json
import re


def format_json_to_data(json_str):
    pattern = r"\{.*\}"
    match = re.search(pattern, json_str, re.DOTALL)

    json_str = match.group(0)


    data = json.loads(json_str)
    output = "<data>\n"
    for key in data.keys():
        items = data[key]
        if not isinstance(items, list):
            items = [str(items)]
        output += f"{key}: {', '.join(items)}\n"
    output += "</data>"
    return output
