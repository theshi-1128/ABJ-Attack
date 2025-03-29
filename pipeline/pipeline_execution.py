from tqdm import tqdm
from utils.clean_text import clean_text
from pipeline.data_preparation import get_data
from pipeline.data_analysis import get_attack_prompt
from pipeline.toxicity_adjustment import toxicity_adjustment
from utils.print_helper import print_response_judgement, print_toxicity_adjustment, print_adjustment_response_judgement


def pipeline_execution(df, judge_prompt, saver, columns, target_model, assist_model, judge_model, max_attack_rounds, max_adjustment_rounds):
    for index, row in tqdm(df.iterrows(), total=df.shape[0], desc="Processing"):
        task = row['goal']
        data = get_data(task, assist_model)
        attack_prompt = get_attack_prompt(data)

        # Perform multiple rounds of attack and judgement
        response = ''
        response_results = []
        judgement_results = []

        # Perform multiple rounds of attack and judgement
        for i in range(max_attack_rounds):
            response = clean_text(target_model.generate_response(attack_prompt))
            judgement = clean_text(judge_model.generate_response(judge_prompt.format(PROMPT=response)))
            print_response_judgement(i, response, judgement)
            judgement_results.append(judgement)
            response_results.append(response)

        if '1' in judgement_results:
            data_values = [task, attack_prompt] + response_results + judgement_results
            data_dict = dict(zip(columns, data_values))
            saver.add_and_save(data_dict)
        # If judgement is 0 (toxicity detected), apply toxicity adjustment and re-attack
        elif '1' not in judgement_results:
            adjustment_rounds = 0
            while adjustment_rounds < max_adjustment_rounds:
                print_toxicity_adjustment(adjustment_rounds)
                data = toxicity_adjustment(response, data, judge_model, assist_model)  # Adjust the data to reduce toxicity
                attack_prompt = get_attack_prompt(data)  # Get new attack prompt
                response_results = []
                judgement_results = []
                for i in range(max_attack_rounds):
                    response = clean_text(target_model.generate_response(attack_prompt))
                    judgement = clean_text(judge_model.generate_response(judge_prompt.format(PROMPT=response)))
                    print_adjustment_response_judgement(i, response, judgement)
                    judgement_results.append(judgement)
                    response_results.append(response)
                if '1' in judgement_results:
                    data_values = [task, attack_prompt] + response_results + judgement_results
                    data_dict = dict(zip(columns, data_values))
                    saver.add_and_save(data_dict)
                    break
                adjustment_rounds += 1
            if adjustment_rounds == max_adjustment_rounds:
                data_values = [task, attack_prompt] + response_results + judgement_results
                data_dict = dict(zip(columns, data_values))
                saver.add_and_save(data_dict)

    # Final save to ensure all data is saved
    saver.final_save()
