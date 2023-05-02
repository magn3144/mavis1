import whisper
import os


def get_text_from_sound():
    model = whisper.load_model('base')
    audio_path = str(os.getcwd()) + '\\searchclient\\tmp\\test.wav'
    text = model.transcribe(audio_path)['text'].lower()
    return text