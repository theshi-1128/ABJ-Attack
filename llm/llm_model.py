from llm.api_config import *
from llm.api import get_response, get_reason_response
from transformers import AutoTokenizer, AutoModelForCausalLM


MODEL_LIST = {
    'qwen2': ['replace with your model_path'],
    'llama3': ['replace with your model_path'],
}


class LLMModel(object):
    def __init__(self, model_name: str, device: str, temperature: float, top_p: float, dtype="auto"):
        self.dtype = dtype  # Set data type
        self.device = device  # Set device
        self.model_name = model_name  # Set model name
        self.temperature = temperature
        self.top_p = top_p
        if self.model_name in ['llama3', 'qwen2']:
            self.model_path = MODEL_LIST[self.model_name][0]  # Get model path from MODEL_LIST
            self.tokenizer, self.model = self._load_model_and_tokenizer()  # Load model and tokenizer

    def _load_model_and_tokenizer(self):
        """
        Load the tokenizer and model based on the model path.

        Returns:
            tuple: A tuple containing the tokenizer and model.
        """
        tokenizer = AutoTokenizer.from_pretrained(self.model_path, torch_dtype=self.dtype, device_map=self.device, use_fast=False, trust_remote_code=True)
        model = AutoModelForCausalLM.from_pretrained(self.model_path, torch_dtype=self.dtype, device_map=self.device, trust_remote_code=True)
        return tokenizer, model

    def generate_response(self, prompt):
        """
        Generate a response based on the provided prompt.

        Args:
            prompt (str): The input text for which the response is to be generated.

        Returns:
            str: The generated response.
        """
        if self.model_name in ['gpt4o', 'claude3_haiku', 'deepseek_v3']:
            temperature = self.temperature
            top_p = self.top_p
            url = base_url
            api_key = model_list[self.model_name]['api_key']
            model = model_list[self.model_name]['model_name']
            response = get_response(prompt, url, api_key, model, temperature, top_p)
            return response
        elif self.model_name in ['o1', 'r1']:
            url = base_url
            api_key = model_list[self.model_name]['api_key']
            model = model_list[self.model_name]['model_name']
            response = get_reason_response(prompt, url, api_key, model)
            return response
        else:
            messages = [
                {"role": "user", "content": prompt}
            ]
            text = self.tokenizer.apply_chat_template(
                messages,
                tokenize=False,
                add_generation_prompt=True
            )
            model_inputs = self.tokenizer([text], return_tensors="pt").to(self.device)
            generated_ids = self.model.generate(
                input_ids=model_inputs.input_ids,
                attention_mask=model_inputs.attention_mask,
                max_new_tokens=8192,
                do_sample=False,
                pad_token_id=self.tokenizer.eos_token_id
            )
            generated_ids = [
                output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
            ]
            response = self.tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
            if "<|assistant|>" in response:
                response = response.split("<|assistant|>")[0].strip()
            if "<|im_end|>" in response:
                response = response.split("<|im_end|>")[0].strip()
            return response