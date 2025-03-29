import argparse
from pipeline.pipeline_execution import pipeline_execution
from pipeline.pipeline_initialization import pipeline_initialization


parser = argparse.ArgumentParser(description='Process input parameters for generating text and judging harmfulness.')
parser.add_argument('--target_model', type=str, default='claude3_5_sonnet', help='[o1, r1, deepseek_v3, gpt4o, qwen2, llama3, claude3_haiku]')
parser.add_argument('--assist_model', type=str, default='qwen2')
parser.add_argument('--judge_model', type=str, default='gpt4o')
parser.add_argument('--dataset_dir', type=str, default='./dataset/harmful_behaviors.csv', help='Directory of the dataset')
parser.add_argument('--save_interval', type=int, default=1 * 1 * 10, help='Interval of saving CSV file')
parser.add_argument('--max_attack_rounds', type=int, default=3, help='Number of iteration rounds')
parser.add_argument('--max_adjustment_rounds', type=int, default=5, help='Number of adjustment rounds')
parser.add_argument('--target_model_cuda_id', type=str, default="cuda:0")
parser.add_argument('--assist_model_cuda_id', type=str, default="cuda:1")
parser.add_argument('--judge_model_cuda_id', type=str, default="cuda:2")
args = parser.parse_args()


if __name__ == '__main__':
    initialize_data = pipeline_initialization(args)
    pipeline_execution(**initialize_data)