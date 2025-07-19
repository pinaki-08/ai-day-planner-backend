import openai

openai.api_key = "your-openai-api-key"

def get_ai_suggestion(tasks):
    prompt = f"Given today's tasks: {tasks}, suggest how to organize them for better productivity."
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response['choices'][0]['message']['content']
