from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
openai_api_key = os.getenv('OPENAI_API')
client = OpenAI(api_key=openai_api_key)

def send_lastmessages_to_openai(Model):
    last_messages = Model.objects.all()
    prompt = """

    Объедени все новости в один пост для телеграма, сделай его кликбейтным 
    Так же удали все ссылки на источники и упоминания об источниках, добавь больше
    эмодзи для кликбейта. Добавь оригинальности
    """
    for message in last_messages:
        prompt += f"\n\n{message.text}"
    
    response = client.chat.completions.create(
         model="gpt-3.5-turbo",
        messages=prompt,
    )
    return response.choices