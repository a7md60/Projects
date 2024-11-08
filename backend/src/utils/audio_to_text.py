from openai import OpenAI
import os

api_key = os.environ.get("OPENAI_KEY")
client = OpenAI(api_key=api_key)

def convert_audio_to_text(audio_file):
    try:

        transcript = client.audio.transcriptions.create(
        model="whisper-1", 
        file=audio_file
        )
        message_text = transcript.text
        return message_text
    except Exception as e:
        print(e)
        return 