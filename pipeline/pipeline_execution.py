from tqdm import tqdm
from pipeline.data_preparation import get_data
from pipeline.data_analysis import get_attack_prompt
from pipeline.toxicity_adjustment import toxicity_adjustment
from utils.print_helper import print_response_judgement, print_toxicity_adjustment, print_adjustment_response_judgement
from utils.text2img import generate_visual_descriptions


def generate_responses_and_judgements(attack_prompt, target_models, judge_model, judge_prompt, max_attack_rounds):
    response_results = [[] for _ in target_models]
    judgement_results = [[] for _ in target_models]
    for i in range(max_attack_rounds):
        for idx, model in enumerate(target_models):
            response = model.generate_response(attack_prompt)
            judgement = judge_model.generate_response(judge_prompt.format(PROMPT=response))

            print_response_judgement(i, response, judgement)

            response_results[idx].append(response)
            judgement_results[idx].append(judgement)
    return response_results, judgement_results


def save_results_if_needed(task, attack_prompt, response_results_list, judgement_results_list, columns, saver):
    data_values = [task, attack_prompt]
    for responses in response_results_list:
        data_values.extend(responses)
    for judgements in judgement_results_list:
        data_values.extend(judgements)
    data_dict = dict(zip(columns, data_values))
    saver.add_and_save(data_dict)


def pipeline_execution(target_models, assist_model, judge_model, df, judge_prompt, saver, columns,
                           max_attack_rounds, max_adjustment_rounds, output_dir):

    for index, row in tqdm(df.iterrows(), total=df.shape[0], desc="Processing"):
        if index == 50:
            break
        task = row['goal']
        data = get_data(task, assist_model)
        attack_prompt = get_attack_prompt(data)

        # First attack and judge
        response_results_list, judgement_results_list = generate_responses_and_judgements(
            attack_prompt, target_models, judge_model, judge_prompt, max_attack_rounds
        )
        if all('1' in judgement_results[0] for judgement_results in judgement_results_list):
            save_results_if_needed(task, attack_prompt, response_results_list, judgement_results_list, columns, saver)
        # If judgement is 0 (toxicity detected), apply toxicity adjustment and re-attack
        else:
            adjustment_rounds = 0
            while adjustment_rounds < max_adjustment_rounds:
                print_toxicity_adjustment(adjustment_rounds)
                data = toxicity_adjustment(response_results_list[0][-1], data, judge_model, assist_model)
                attack_prompt = get_attack_prompt(data)

                response_results_list, judgement_results_list = generate_responses_and_judgements(
                    attack_prompt, target_models, judge_model, judge_prompt, max_attack_rounds
                )

                if all('1' in judgement_results[0] for judgement_results in judgement_results_list):
                    save_results_if_needed(task, attack_prompt, response_results_list, judgement_results_list, columns,
                                           saver)
                    break

                adjustment_rounds += 1

            if adjustment_rounds == max_adjustment_rounds:
                save_results_if_needed(task, attack_prompt, response_results_list, judgement_results_list, columns,
                                       saver)

    saver.final_save()
    # generate_visual_descriptions(
    #     llm=assist_model,
    #     input_csv_path=output_dir,
    # )
