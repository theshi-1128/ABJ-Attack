from openai import OpenAI


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
            max_tokens=8192,
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
