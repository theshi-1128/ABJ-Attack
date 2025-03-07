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
    
- We uncover the security risks in state-of-the-art LLMs during complex reasoning process and propose Analyzing-based Jailbreak (ABJ), a novel and efficient jailbreak attack method designed to assess these vulnerabilities.
- We conduct comprehensive experiments on state-of-the-art open-source and closed-source LLMs. The experimental results demonstrate that ABJ exhibits exceptional attack effectiveness, transferability, and efficiency across different LLMs compared to other baselines.
- We demonstrate the robustness and flexibility of ABJ and reveal the reason why it outperforms other baselines. Additionally, we discuss several efficient defense strategies to mitigate ABJ without compromising the model's reasoning capabilities.


<p align="center">
  <img src="acl_figure_1.png" width="900"/>
</p>


## Argument Specification

- `attack_method`: We implement `4` kind of ABJ Attack, including `original_ABJ`, `modified_ABJ`, `code_based_ABJ`,`adversarial_ABJ`.
  
- `target_model`: The name of target model.
  
- `attack_rounds`: Number of iteration rounds, default is `3`.
  
- `target_model_cuda_id`: Number of the GPU for target model, default is `cuda:0`.

  
## Quick Start

Before you start, you should replace the necessary information in `llm/api_config.py` and `llm/llm_model.py`.


1. Clone this repository:

   ```sh
   git clone https://github.com/theshi-1128/ABJ-Attack.git
   ```

2. Build enviroment:

   ```sh
   cd ABJ-Attack
   conda create -n ABJ python==3.10
   conda activate ABJ
   pip install -r requirements.txt
   ```

3. Run ABJ-Attack:

     ```sh
     python ABJ.py \
     -- attack_method [ATTACK METHOD] \
     -- target_model [TARGET MODEL] \
     -- attack_rounds [ATTACK ROUNDS] \
     -- target_model_cuda_id [CUDA ID]
     ```

    For example, to run `original_ABJ` with `gpt-4-turbo-2024-04-09` as the target model on `CUDA:0` for `3` rounds, run
  
     ```sh
     python ABJ.py \
     -- attack_method original_ABJ \
     -- target_model gpt4 \
     -- attack_rounds 3 \
     -- target_model_cuda_id cuda:1
     ```



## Citation

If you find this work useful in your own research, please feel free to leave a star⭐️ and cite our paper:

```bibtex
@article{lin2024figure,
  title={LLMs can be Dangerous Reasoners: Analyzing-based Jailbreak Attack on Large Language Models},
  author={Lin, Shi and Yang, Hongming and Lin, Dingyang and Li, Rongchang and Wang, Xun and Lin, Changting and Xing, Wenpeng and Han, Meng},
  journal={arXiv preprint arXiv:2407.16205},
  year={2024}
}
```
