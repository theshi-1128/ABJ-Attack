from openai import OpenAI
import base64


def get_response(prompt, url, api_key, model_name, temperature, top_p):
    client = OpenAI(
        base_url=url,
        api_key=api_key
    )
    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=temperature,
            top_p=top_p,
        )
        return response.choices[0].message.content
    except Exception as e:
        return str(e)


def get_reason_response(prompt, url, api_key, model_name):
    client = OpenAI(
        base_url=url,
        api_key=api_key
    )
    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "user", "content": prompt}
            ],
        )
        return response.choices[0].message.content
    except Exception as e:
        return str(e)


def get_img(prompt, url, api_key, model_name):
    client = OpenAI(
        base_url=url,
        api_key=api_key
    )
    try:
        img = client.images.generate(
            model=model_name,
            prompt=prompt,
            n=1,
            size="1024x1024",
        )
        image_bytes = base64.b64decode(img.data[0].b64_json)
        return image_bytes
    except Exception as e:
        return str(e)


def get_image_response(prompt, image_path, url, api_key, model_name, temperature, top_p):
    client = OpenAI(
        base_url=url,
        api_key=api_key
    )
    try:
        with open(image_path, "rb") as image_file:
            base64_image = base64.b64encode(image_file.read()).decode("utf-8")
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            temperature=temperature,
            top_p=top_p,
        )

        return response.choices[0].message.content
    except Exception as e:
        return str(e)
