from gpt.summarize import send_lastmessages_to_openai
from .models import TelegramChanell, LastMessages

def get_news_channels(client):
    channels = TelegramChanell.objects.all()
    last_messages = {}
    for channel in channels:
        entity = client.get_entity(channel.id)
        message = client.get_messages(entity, limit=1)[0]

        media = None
        if message.photo: 
            media = message.photo
        elif message.video:
            media = message.video
        elif message.document:
            media = message.document
        last_messages[channel.id] = {
            'text': message.text,
            'source': channel.name,
            'datetime': message.date.isoformat(),
            'media': media
        }
    
    for channel_id, message_data in last_messages.items():
        LastMessages.objects.update_or_create(
            channel_id=channel_id,
            defaults={
                'text': message_data['text'],
                'date': message_data['datetime'],
            }
        )
    results = send_lastmessages_to_openai(LastMessages)

    print(results)
