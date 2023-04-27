import whisper
import os

model = whisper.load_model('base')

audio_path = str(os.getcwd()) + '\\searchclient\\tmp\\test.wav'
print(audio_path)
text = model.transcribe(audio_path)['text'].lower()
print(text)