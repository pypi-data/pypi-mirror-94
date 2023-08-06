import librosa
import soundfile as sf
import torch
from transformers import Wav2VecForCTC, Wav2Vec2Tokenizer


if __name__ == "__main__":
    tokenizer = Wav2Vec2Tokenizer.from_pretrained("facebook/wav2vec2-base-960h")
    model = Wav2VecForCTC.from_pretrained("facebook/wav2vec2-base-960h")
    speech, rate = sf.read("sample.wav")
    speech = librosa.resample(speech, rate, 16000)
    input_values = tokenizer(speech, return_tensors="pt").input_values
    logits = model(input_values).logits
    predicted_ids = torch.argmax(logits, dim=-1)
    transcription = tokenizer.decode(predicted_ids[0])
    print(transcription)
