import json


def format_json_to_data(json_str):
    if json_str.startswith("```json"):
        json_str = json_str[7:].strip()
    if json_str.endswith("```"):
        json_str = json_str[:-3].strip()
    data = json.loads(json_str)
    output = "<data>\n"
    for key in data.keys():
        items = data[key]
        if not isinstance(items, list):
            items = [str(items)]
        output += f"{key}: {', '.join(items)}\n"
    output += "</data>"
    return output