import pandas as pd
import re
from tqdm import tqdm
from utils.print_helper import print_description, print_prompt


def generate_visual_descriptions(
    llm,
    input_csv_path: str,
):
    df = pd.read_csv(input_csv_path)
    responses = []

    for idx, row in tqdm(df.iterrows(), total=len(df), desc="Generating descriptions"):
        prompt_text = row['prompt']
        match = re.search(r"(<data>[\s\S]*?</data>)", prompt_text)

        if match:
            data_block = match.group(1)
            full_prompt = f"{data_block}\n\nPlease write a single paragraph visual scene description based on the above text data, with a length of about 150 words in English."
            try:
                res = llm.generate_response(full_prompt)
            except Exception as e:
                res = f"ERROR: {str(e)}"
        else:
            full_prompt = "NO <data> FOUND"
            res = "SKIPPED"

        print_prompt(full_prompt)
        print_description(res)

        responses.append(res)

    df['img_description'] = responses
    df.to_csv(input_csv_path, index=False, encoding='utf-8')
    print(f"✅ Done. Output updated in {input_csv_path}")
