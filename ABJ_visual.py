import argparse
from pipeline.pipeline_execution_img import pipeline_execution
from pipeline.pipeline_initialization_img import pipeline_initialization
from llm.llm_model import LLMModel
from utils.print_helper import print_judge_model, print_assist_model, print_target_model_1, print_target_model_2, print_target_model_3, print_target_model_4


parser = argparse.ArgumentParser(description='Process input parameters for generating text and judging harmfulness.')
parser.add_argument('--num_target_models', type=int, default=1)
parser.add_argument('--target_model', type=str, default='gpt4o_vl', help='[gpt4o_vl]')
parser.add_argument('--assist_model_text', type=str, default='glm4')
parser.add_argument('--assist_model_img', type=str, default='gpt_img')
parser.add_argument('--judge_model', type=str, default='gpt4o')
parser.add_argument('--dataset_dir', type=str, default='./dataset/harmful_behaviors.csv', help='Directory of the dataset')
parser.add_argument('--save_interval', type=int, default=1 * 1 * 10, help='Interval of saving CSV file')
parser.add_argument('--max_attack_rounds', type=int, default=1, help='Number of iteration rounds')
parser.add_argument('--max_adjustment_rounds', type=int, default=3, help='Number of adjustment rounds')
parser.add_argument('--target_model_cuda_id', type=str, default="cuda:0")
parser.add_argument('--assist_model_cuda_id', type=str, default="cuda:1")
parser.add_argument('--judge_model_cuda_id', type=str, default="cuda:2")
args = parser.parse_args()


if __name__ == '__main__':
    target_models = []
    # Load the target model
    target_model = LLMModel(model_name=args.target_model, device=args.target_model_cuda_id, temperature=0, top_p=0)
    print_target_model_1(args.target_model)
    target_models.append(target_model)

    # Load the assist model
    assist_model_text = LLMModel(model_name=args.assist_model_text, device=args.assist_model_cuda_id, temperature=1, top_p=1)
    print_assist_model(args.assist_model_text)

    # Load the assist model
    assist_model_img = LLMModel(model_name=args.assist_model_img, device=args.assist_model_cuda_id)
    print_assist_model(args.assist_model_img)

    # Load the judge model
    judge_model = LLMModel(model_name=args.judge_model, device=args.judge_model_cuda_id, temperature=0, top_p=0)
    print_judge_model(args.judge_model)

    initialize_data = pipeline_initialization(args)
    pipeline_execution(target_models, assist_model_text, assist_model_img, judge_model, **initialize_data)
