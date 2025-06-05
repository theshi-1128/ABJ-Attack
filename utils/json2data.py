import json
import re


def format_json_to_data(json_str: str) -> str:
    """Convert a JSON string to the <data> format used by the pipeline.

    The model responses are not always guaranteed to be valid JSON. This
    function extracts the JSON portion and converts it to the expected
    ``<data>`` block. If no JSON can be found or parsed, the original string is
    returned unchanged so the caller can decide how to handle it.
    """

    pattern = r"\{.*\}"
    match = re.search(pattern, json_str, re.DOTALL)
    if not match:
        # Return original text when no JSON structure is detected
        return json_str

    json_part = match.group(0)
    try:
        data = json.loads(json_part)
    except json.JSONDecodeError:
        # If parsing fails, fall back to the raw JSON string
        return json_str

    output = "<data>\n"
    for key, items in data.items():
        if isinstance(items, list):
            items = [str(item) for item in items]
        else:
            items = [str(items)]
        output += f"{key}: {', '.join(items)}\n"
    output += "</data>"
    return output

