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


def print_target_model(model):
    print("-"*125)
    print("Target Model:\n", model)
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
