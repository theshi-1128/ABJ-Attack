# ABJ-Attack
This repository contains official implementation of our paper "[LLMs can be Dangerous Reasoners: Analyzing-based Jailbreak Attack on Large Language Models](https://arxiv.org/pdf/2407.16205v4)"

[![arXiv: paper](https://img.shields.io/badge/arXiv-paper-red.svg)](https://arxiv.org/abs/2407.16205)
![Jailbreak Attacks](https://img.shields.io/badge/Jailbreak-Attacks-yellow.svg?style=plastic)
![Large Language Models](https://img.shields.io/badge/LargeLanguage-Models-green.svg?style=plastic)
[![license: MIT](https://img.shields.io/badge/license-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Please feel free to contact linshizjgsu@gmail.com if you have any questions.

## Table of Contents

- [Updates](#updates)
- [Overview](#overview)
- [Argument Specification](#argument-specification)
- [Quick Start](#quick-start)


## Updates

- (**2024/07/21**) We have released the official code of ABJ-Attack!
- (**2024/07/23**) Our paper is on arXiv! Check it out [here](https://arxiv.org/abs/2407.16205v4)!
- (**2024/09/11**) We have released a comprehensive defense methodology against jailbreak attacks！Check it out [here](https://github.com/theshi-1128/llm-defense)!
- (**2024/09/26**) We have released a simple yet comprehensive benchmark that covers most of the existing jailbreak attack methods！Check it out [here](https://github.com/theshi-1128/jailbreak-bench)!


## Overview

This repository shares the code of our latest work on LLMs jailbreaking. In this work:
    
- We investigate a novel jailbreak attack paradigm that transitions from input-level obfuscation to reasoning-level manipulation, unveiling a previously overlooked attack surface inherent in the chain-of-thought reasoning trajectory of LLMs.
- We present Analyzing-based Jailbreak (ABJ), a black-box attack method that steers the model's reasoning chains towards harmful outputs. ABJ introduces multimodal attack paths, effectively exploiting and exposing the intrinsic vulnerabilities within the textual and visual reasoning process of current LLMs.
- We conduct extensive experiments to evaluate ABJ against diverse LLMs, demonstrating its impressive attack performance in terms of attack effectiveness, efficiency, and transferability. Additionally, we analyze the key factors contributing to ABJ's effectiveness and discuss potential defense strategies.


<p align="center">
  <img src="overview.pdf" width="900"/>
</p>


## Argument Specification
  
- `target_model`: The name of target model.

- `assist_model`: The name of assist model.

- `judge_model`: The name of judge model.
  
- `max_attack_rounds`: Number of attack iteration rounds, default is `3`.

- `max_adjustment_rounds`: Number of toxicity adjustment rounds, default is `5`.

- `target_model_cuda_id`: Number of the GPU for target model, default is `cuda:0`.

- `assist_model_cuda_id`: Number of the GPU for assist model, default is `cuda:1`.

- `judge_model_cuda_id`: Number of the GPU for judge model, default is `cuda:2`.

  
## Quick Start

Before you start, you should replace the necessary information(`api_key`, `url`, `model_path`) in `llm/api_config.py` and `llm/llm_model.py`.


1. Clone this repository:

   ```sh
   git clone https://github.com/theshi-1128/ABJ-Attack.git
   ```

2. Build enviroment:

   ```sh
   cd ABJ-Attack
   conda create -n ABJ python==3.11
   conda activate ABJ
   pip install -r requirements.txt
   ```

3. Run ABJ-Attack:

     ```sh
     python ABJ.py \
     -- target_model [TARGET MODEL] \
     -- max_attack_rounds [ATTACK ROUNDS] \
     -- target_model_cuda_id [CUDA ID]
     ```

    For example, to run `ABJ` with `gpt-4o-2024-11-20` as the target model on `CUDA:0` for `3` rounds, run
  
     ```sh
     python ABJ.py \
     -- target_model gpt4o \
     -- max_attack_rounds 3 \
     -- target_model_cuda_id cuda:1
     ```



## Citation

If you find this work useful in your own research, please feel free to leave a star⭐️ and cite our paper:

```bibtex
@article{lin2024figure,
  title={LLMs can be Dangerous Reasoners: Analyzing-based Jailbreak Attack on Large Language Models},
  author={Lin, Shi and Yang, Hongming and Li, Rongchang and Wang, Xun and Lin, Changting and Xing, Wenpeng and Han, Meng},
  journal={arXiv preprint arXiv:2407.16205},
  year={2024}
}
```
