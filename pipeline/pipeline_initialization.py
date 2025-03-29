import pandas as pd
from llm.llm_model import LLMModel
from utils.interval_saver import IntervalSaver
from utils.print_helper import print_judge_model, print_assist_model, print_target_model
from pipeline.pipeline_prompt import judge_prompt


def pipeline_initialization(args):
    # Load the target model
    llm_model = LLMModel(model_name=args.target_model, device=args.target_model_cuda_id, temperature=0, top_p=0)
    print_target_model(args.target_model)

    # Load the assist model
    assist_model = LLMModel(model_name=args.assist_model, device=args.assist_model_cuda_id, temperature=1, top_p=1)
    print_assist_model(args.assist_model)

    # Load the judge model
    judge_model = LLMModel(model_name=args.judge_model, device=args.judge_model_cuda_id, temperature=0, top_p=0)
    print_judge_model(args.judge_model)

    # Define column names for the DataFrame
    columns = ['task', 'prompt'] + \
              [f'output{i}' for i in range(1, args.max_attack_rounds + 1)] + \
              [f'label{i}' for i in range(1, args.max_attack_rounds + 1)]

    # Read the dataset from the specified directory
    df = pd.read_csv(args.dataset_dir)

    output_dir = f'./output/{args.target_model}.csv'

    # Initialize the IntervalSaver for saving outputs at specified intervals
    saver = IntervalSaver(output_dir, interval=args.save_interval, columns=columns)

    return {
        'df': df,
        'judge_prompt': judge_prompt,
        'saver': saver,
        'columns': columns,
        'target_model': llm_model,
        'assist_model': assist_model,
        'judge_model': judge_model,
        'max_attack_rounds': args.max_attack_rounds,
        'max_adjustment_rounds': args.max_adjustment_rounds
    }