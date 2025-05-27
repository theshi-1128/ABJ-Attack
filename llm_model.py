from llm.api import get_response, get_reason_response, get_img, get_image_response
from llm.api_config import *
from transformers import AutoTokenizer, AutoModelForCausalLM, AutoProcessor, AutoModel
# from transformers import Qwen2_5_VLForConditionalGeneration
import torch
import torchvision.transforms as T
from PIL import Image
from torchvision.transforms.functional import InterpolationMode
from qwen_vl_utils import process_vision_info


MODEL_LIST = {
    'qwen2': ['replace with your model_path'],
    'llama3': ['replace with your model_path'],
    'intern3_vl': ['replace with your model_path'],
    'qwen2_5_vl': ['replace with your model_path']
}


def build_transform(input_size):
    IMAGENET_MEAN = (0.485, 0.456, 0.406)
    IMAGENET_STD = (0.229, 0.224, 0.225)
    MEAN, STD = IMAGENET_MEAN, IMAGENET_STD
    transform = T.Compose([
        T.Lambda(lambda img: img.convert('RGB') if img.mode != 'RGB' else img),
        T.Resize((input_size, input_size), interpolation=InterpolationMode.BICUBIC),
        T.ToTensor(),
        T.Normalize(mean=MEAN, std=STD)
    ])
    return transform


def find_closest_aspect_ratio(aspect_ratio, target_ratios, width, height, image_size):
    best_ratio_diff = float('inf')
    best_ratio = (1, 1)
    area = width * height
    for ratio in target_ratios:
        target_aspect_ratio = ratio[0] / ratio[1]
        ratio_diff = abs(aspect_ratio - target_aspect_ratio)
        if ratio_diff < best_ratio_diff:
            best_ratio_diff = ratio_diff
            best_ratio = ratio
        elif ratio_diff == best_ratio_diff:
            if area > 0.5 * image_size * image_size * ratio[0] * ratio[1]:
                best_ratio = ratio
    return best_ratio


def dynamic_preprocess(image, min_num=1, max_num=12, image_size=448, use_thumbnail=False):
    orig_width, orig_height = image.size
    aspect_ratio = orig_width / orig_height

    # calculate the existing image aspect ratio
    target_ratios = set(
        (i, j) for n in range(min_num, max_num + 1) for i in range(1, n + 1) for j in range(1, n + 1) if
        i * j <= max_num and i * j >= min_num)
    target_ratios = sorted(target_ratios, key=lambda x: x[0] * x[1])

    # find the closest aspect ratio to the target
    target_aspect_ratio = find_closest_aspect_ratio(
        aspect_ratio, target_ratios, orig_width, orig_height, image_size)

    # calculate the target width and height
    target_width = image_size * target_aspect_ratio[0]
    target_height = image_size * target_aspect_ratio[1]
    blocks = target_aspect_ratio[0] * target_aspect_ratio[1]

    # resize the image
    resized_img = image.resize((target_width, target_height))
    processed_images = []
    for i in range(blocks):
        box = (
            (i % (target_width // image_size)) * image_size,
            (i // (target_width // image_size)) * image_size,
            ((i % (target_width // image_size)) + 1) * image_size,
            ((i // (target_width // image_size)) + 1) * image_size
        )
        # split the image
        split_img = resized_img.crop(box)
        processed_images.append(split_img)
    assert len(processed_images) == blocks
    if use_thumbnail and len(processed_images) != 1:
        thumbnail_img = image.resize((image_size, image_size))
        processed_images.append(thumbnail_img)
    return processed_images


def load_image(image_file, input_size=448, max_num=12):
    image = Image.open(image_file).convert('RGB')
    transform = build_transform(input_size=input_size)
    images = dynamic_preprocess(image, image_size=input_size, use_thumbnail=True, max_num=max_num)
    pixel_values = [transform(image) for image in images]
    pixel_values = torch.stack(pixel_values)
    return pixel_values


class LLMModel(object):
    def __init__(self, model_name: str, device: str, temperature: float=None, top_p: float=None, dtype="auto"):
        self.dtype = dtype  # Set data type
        self.device = device  # Set device
        self.model_name = model_name  # Set model name
        self.temperature = temperature
        self.top_p = top_p
        if self.model_name in ['qwen2_5_vl']:
            self.model_path = MODEL_LIST[self.model_name][0]  # Get model path from MODEL_LIST
            self.tokenizer, self.model = self._load_model_and_tokenizer()  # Load model and tokenizer
        elif self.model_name in ['llama3', 'qwen2', 'intern3_vl']:
            self.model_path = MODEL_LIST[self.model_name][0]  # Get model path from MODEL_LIST
            self.model, self.processor = self._load_model_and_tokenizer()  # Load model and tokenizer

    def _load_model_and_tokenizer(self):
            """
            Load the tokenizer and model based on the model path.

            Returns:
                tuple: A tuple containing the tokenizer and model.
            """
            if self.model_name in ['llama3', 'qwen2']:
                tokenizer = AutoTokenizer.from_pretrained(self.model_path, torch_dtype=self.dtype, device_map=self.device, use_fast=False, trust_remote_code=True)
                model = AutoModelForCausalLM.from_pretrained(self.model_path, torch_dtype=self.dtype, device_map=self.device, trust_remote_code=True)
                return tokenizer, model
            elif self.model_name in ['intern3_vl']:
                model = AutoModel.from_pretrained(
                    self.model_path,
                    torch_dtype=torch.bfloat16,
                    device_map=self.device,
                    low_cpu_mem_usage=True,
                    use_flash_attn=True,
                    trust_remote_code=True).eval()
                tokenizer = AutoTokenizer.from_pretrained(self.model_path, trust_remote_code=True, device_map=self.device, use_fast=False)
                return tokenizer, model
            elif self.model_name in ['qwen2_5_vl']:
                model = Qwen2_5_VLForConditionalGeneration.from_pretrained(self.model_path, torch_dtype=self.dtype, device_map=self.device)
                processor = AutoProcessor.from_pretrained(self.model_path)
                return model, processor

    def generate_response(self, prompt, img=None):
        """
        Generate a response based on the provided prompt.

        Args:
            prompt (str): The input text for which the response is to be generated.

        Returns:
            str: The generated response.
        """
        if self.model_name in ['gpt4o_vl']:
            temperature = self.temperature
            top_p = self.top_p
            url = model_list[self.model_name]['base_url']
            api_key = model_list[self.model_name]['api_key']
            model = model_list[self.model_name]['model_name']
            response = get_image_response(prompt, img, url, api_key, model, temperature, top_p)
            return response
        elif self.model_name in ['gpt4o', 'claude3_haiku', 'deepseek_v3', 'glm4']:
            temperature = self.temperature
            top_p = self.top_p
            url = model_list[self.model_name]['base_url']
            api_key = model_list[self.model_name]['api_key']
            model = model_list[self.model_name]['model_name']
            response = get_response(prompt, url, api_key, model, temperature, top_p)
            return response
        elif self.model_name in ['o1', 'r1']:
            url = model_list[self.model_name]['base_url']
            api_key = model_list[self.model_name]['api_key']
            model = model_list[self.model_name]['model_name']
            response = get_reason_response(prompt, url, api_key, model)
            return response
        elif self.model_name in ['gpt_img']:
            url = model_list[self.model_name]['base_url']
            api_key = model_list[self.model_name]['api_key']
            model = model_list[self.model_name]['model_name']
            response = get_img(prompt, url, api_key, model)
            return response
        elif self.model_name in ['llama3', 'qwen2']:
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
        elif self.model_name in ['qwen2_5_vl']:
            messages = [
                {
                    "role": "user", "content": [
                        {"type": "image", "image": "file://" + img},
                        {"type": "text", "text": prompt},
                    ],
                }
            ]
            # Preparation for inference
            text = self.processor.apply_chat_template(
                messages, tokenize=False, add_generation_prompt=True
            )
            image_inputs, video_inputs = process_vision_info(messages)
            inputs = self.processor(
                text=[text],
                images=image_inputs,
                videos=video_inputs,
                padding=True,
                return_tensors="pt",
            ).to(self.device)

            # Inference: Generation of the output
            generated_ids = self.model.generate(**inputs, max_new_tokens=2048, do_sample=False)
            generated_ids_trimmed = [
                out_ids[len(in_ids):] for in_ids, out_ids in zip(inputs.input_ids, generated_ids)
            ]
            output_text = self.processor.batch_decode(
                generated_ids_trimmed, skip_special_tokens=True, clean_up_tokenization_spaces=False
            )
            return output_text[0]
        elif self.model_name in ['intern3_vl']:
            # set the max number of tiles in `max_num`
            pixel_values = load_image(img, max_num=12).to(torch.bfloat16).to(self.device)
            generation_config = dict(max_new_tokens=2048, do_sample=False, pad_token_id=self.tokenizer.eos_token_id)

            question = '<image>\n' + prompt
            response = self.model.chat(self.tokenizer, pixel_values, question, generation_config)
            return response
