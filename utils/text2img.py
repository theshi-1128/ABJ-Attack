from utils.print_helper import print_description
from pipeline.pipeline_prompt import visual_description_generation


def generate_visual_descriptions(
    data: str,
    llm
):
    full_prompt = f"{data}\n\n{visual_description_generation}"
    try:
        res = llm.generate_response(full_prompt)
    except Exception as e:
        res = f"ERROR: {str(e)}"
    print_description(res)
    return res

