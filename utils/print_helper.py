def print_task(task):
    print("*" * 125)
    print(f"Task: \n{task}")
    print("*" * 125)


def print_rewrite_task(task):
    print("*" * 125)
    print(f"Rewrite Task: \n{task}")
    print("*" * 125)


def print_prompt(prompt):
    print("*" * 125)
    print(f"Full Prompt: \n{prompt}")
    print("*" * 125)

def print_response_judgement(i, response, judgement):
    print(f"Response {i + 1}:\n", response)
    print("-"*125)
    print(f"Judgement {i + 1}:\n", judgement)
    print("-"*125)


def print_toxicity_adjustment(i):
    print("*"*125)
    print(f"Toxicity Adjustment {i + 1}")
    print("*"*125)


def print_adjustment_response_judgement(i, response, judgement):
    print(f"New Response {i + 1}:\n", response)
    print("-"*125)
    print(f"New Judgement {i + 1}:\n", judgement)
    print("-"*125)


def print_attack(attack_prompt):
    print("*"*125)
    print("*"*125)
    print("Attack Prompt:", attack_prompt)
    print("-"*125)


def print_target_model_1(model):
    print("-"*125)
    print("Target Model 1:\n", model)
    print("-"*125)


def print_target_model_2(model):
    print("-"*125)
    print("Target Model 2:\n", model)
    print("-"*125)


def print_target_model_3(model):
    print("-"*125)
    print("Target Model 3:\n", model)
    print("-"*125)


def print_target_model_4(model):
    print("-"*125)
    print("Target Model 4:\n", model)
    print("-"*125)

def print_assist_model(model):
    print("-"*125)
    print("Assist Model:\n", model)
    print("-"*125)


def print_judge_model(model):
    print("-"*125)
    print("Judge Model:\n", model)
    print("-"*125)


def print_judgment(judgment):
    if judgment == '0':
        print("*"*125)
        print("Constructive Response! Needs Toxicity Enhancement!")
        print("*"*125)
    elif judgment == '1':
        print("*"*125)
        print("Refusal Response! Needs Toxicity Reduction!")
        print("*"*125)


def print_description(res):
    print("*"*125)
    print(f"IMG Description:\n", res)
    print("*"*125)
