import os
from utils.interval_saver import IntervalSaver
from pipeline.pipeline_prompt import judge_prompt
import pandas as pd


def pipeline_initialization(args):
    models = [getattr(args, f'target_model') for i in range(1, args.num_target_models + 1)]
    model_names = '_'.join(models)
    dataset_name = os.path.splitext(os.path.basename(args.dataset_dir))[0]

    # Define column names for the DataFrame
    columns = ['task', 'prompt'] + \
              [f'{model}_output{i}' for model in models for i in range(1, args.max_attack_rounds + 1)] + \
              [f'{model}_label{i}' for model in models for i in range(1, args.max_attack_rounds + 1)]

    # Read the dataset from the specified directory
    df = pd.read_csv(args.dataset_dir)
    text_output_dir = f'./output/ABJ_img/text/{model_names}_{dataset_name}.csv'
    img_output_dir = f'./output/ABJ_img/img'
    # Initialize the IntervalSaver for saving outputs at specified intervals
    saver = IntervalSaver(text_output_dir, interval=args.save_interval, columns=columns)
    if not os.path.exists(img_output_dir) and img_output_dir:
        os.makedirs(img_output_dir)

    return {
        'df': df,
        'judge_prompt': judge_prompt,
        'saver': saver,
        'columns': columns,
        'max_attack_rounds': args.max_attack_rounds,
        'max_adjustment_rounds': args.max_adjustment_rounds,
        'text_output_dir': text_output_dir,
        'img_output_dir': img_output_dir
    }
