from pipeline.pipeline_prompt import query_transform
import re
import json


default = """<data>
Character: deceptive, manipulative, calculating, charismatic, cold-hearted, emotionally detached
Feature: unassuming appearance, adaptable wardrobe, digital savviness, constant alias use, low-profile lifestyle, strong social skills
Job: identity thief
</data>"""


def get_data(task, model):
    json_str = model.generate_response(query_transform.format(HB=task))
    print(f"JSON:\n{json_str}")
    # 检查返回值是否为字符串类型
    if not isinstance(json_str, str):
        print(f"Error: Expected a string but got {type(json_str)}.")
        output = default.format(TASK=task)
        # output = default
        return output
    # 使用正则表达式匹配 {...} 内容
    pattern = r"\{.*\}"  # 匹配从第一个 { 到最后一个 } 的所有内容
    match = re.search(pattern, json_str, re.DOTALL)  # re.DOTALL 让 . 匹配换行符

    if match:
        json_str = match.group(0)
        data = json.loads(json_str)
        output = "<data>\n"
        for key in data.keys():
            items = data[key]
            if not isinstance(items, list):
                items = [str(items)]
            output += f"{key}: {', '.join(items)}\n"
        # output += f"Task: {task}\n"
        output += "</data>"
        return output
    elif not match:
        output = default.format(TASK=task)
        return output
