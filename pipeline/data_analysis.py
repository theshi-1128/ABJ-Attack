from utils.print_helper import print_attack
from pipeline.pipeline_prompt import ABJ_attack_prompt, ABJ_visual_attack_prompt


def get_attack_prompt(data):
    attack_prompt = ABJ_attack_prompt.format(DATA=data)
    print_attack(attack_prompt)
    return attack_prompt


def get_visual_attack_prompt():
    attack_prompt = ABJ_visual_attack_prompt
    print_attack(ABJ_visual_attack_prompt)
    return attack_prompt